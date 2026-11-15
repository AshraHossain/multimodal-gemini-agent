"""Test suite for the Multimodal Gemini Agent.

All unit and integration tests run offline using deterministic policies/fakes so
no live Gemini API key or MongoDB Atlas cluster is required for `uv run pytest`.
Live evaluation tests are marked `@pytest.mark.live` and run via `uv run pytest -m live`.
"""
from __future__ import annotations

import base64
import os
from typing import Any

import pytest
from pydantic import ValidationError

from app.models.schemas import AskRequest, AskResponse, IngestResponse
from app.services import atlas, gemini
from app.services.atlas import vector_search_pipeline
from app.services.embedding import cosine_similarity, rank_by_similarity, to_vector


@pytest.fixture(autouse=True)
def _clean_offline_environment(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Force offline deterministic mode unless running a `@pytest.mark.live` test."""
    if request.node.get_closest_marker("live") is None:
        monkeypatch.setenv("GEMINI_MOCK", "1")
        monkeypatch.setenv("ATLAS_MOCK", "1")
    atlas.reset_memory_store()


def _client():
    """Build a FastAPI TestClient."""
    from fastapi.testclient import TestClient

    from app.main import app

    return TestClient(app)


# --- schemas (pure, unit) -----------------------------------------------------
@pytest.mark.unit
def test_ask_request_defaults_top_k():
    assert AskRequest(question="hi").top_k == 4


@pytest.mark.unit
def test_ask_request_accepts_image():
    assert AskRequest(question="q", image_b64="YWJj").image_b64 == "YWJj"


@pytest.mark.unit
def test_ask_response_sources_default_empty():
    assert AskResponse(answer="a").sources == []


@pytest.mark.unit
def test_ingest_response_fields():
    r = IngestResponse(doc_id="d1", chunks=3)
    assert r.doc_id == "d1" and r.chunks == 3


@pytest.mark.unit
def test_ask_request_rejects_missing_question():
    with pytest.raises(ValidationError):
        AskRequest()  # type: ignore[call-arg]


@pytest.mark.unit
def test_schemas_are_immutable():
    req = AskRequest(question="immutable?")
    with pytest.raises(ValidationError):
        req.question = "mutated"  # type: ignore[misc]


# --- atlas pipeline builder & collection store (unit) -------------------------
@pytest.mark.unit
def test_pipeline_has_vector_search_stage():
    p = vector_search_pipeline([0.1, 0.2], k=4)
    assert p[0].get("$vectorSearch") is not None


@pytest.mark.unit
def test_pipeline_limit_matches_k():
    p = vector_search_pipeline([0.0], k=7)
    assert p[0]["$vectorSearch"]["limit"] == 7


@pytest.mark.unit
def test_pipeline_num_candidates_scales_with_k():
    p = vector_search_pipeline([0.0], k=5)
    assert p[0]["$vectorSearch"]["numCandidates"] == 50


@pytest.mark.unit
def test_pipeline_uses_custom_index_name():
    p = vector_search_pipeline([0.0], index="my_index")
    assert p[0]["$vectorSearch"]["index"] == "my_index"


@pytest.mark.unit
def test_pipeline_path_is_embedding():
    p = vector_search_pipeline([0.0])
    assert p[0]["$vectorSearch"]["path"] == "embedding"


@pytest.mark.unit
def test_atlas_store_and_search_with_injected_collection():
    inserted: list[dict[str, Any]] = []

    class FakeCollection:
        def insert_one(self, doc: dict[str, Any]) -> None:
            inserted.append(doc)

        def aggregate(self, pipeline: list[dict[str, Any]]) -> list[dict[str, Any]]:
            assert pipeline[0]["$vectorSearch"]["index"] == "custom_idx"
            return inserted

    coll = FakeCollection()
    rec = atlas.store_document("chart caption", [0.5, 0.5], doc_id="c1", collection=coll)
    assert rec["doc_id"] == "c1"
    results = atlas.search_similar([0.5, 0.5], k=2, index="custom_idx", collection=coll)
    assert len(results) == 1 and results[0]["doc_id"] == "c1"


# --- API routes (integration, offline) ----------------------------------------
@pytest.mark.integration
def test_health_ok():
    assert _client().get("/health").json() == {"status": "ok"}


@pytest.mark.integration
def test_health_status_code():
    assert _client().get("/health").status_code == 200


@pytest.mark.integration
def test_ingest_returns_doc_id():
    payload = {"image_b64": base64.b64encode(b"fake-chart-bytes").decode("ascii")}
    resp = _client().post("/ingest", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["doc_id"].startswith("doc-")
    assert body["chunks"] == 1


@pytest.mark.integration
def test_ingest_multipage_pdf_splits_into_page_chunks():
    sample_pdf = (
        b"%PDF-1.7\n"
        b"1 0 obj << /Type /Pages /Count 3 >> endobj\n"
        b"2 0 obj << /Type /Page /Contents (Page 1 revenue chart) >> endobj\n"
        b"3 0 obj << /Type /Page /Contents (Page 2 margin diagram) >> endobj\n"
        b"4 0 obj << /Type /Page /Contents (Page 3 forecast table) >> endobj\n"
    )
    client = _client()
    files = {"file": ("quarterly_report.pdf", sample_pdf, "application/pdf")}
    resp = client.post("/ingest", files=files)
    assert resp.status_code == 200
    body = resp.json()
    assert body["doc_id"] == "quarterly_report.pdf"
    assert body["chunks"] == 3

    ask_resp = client.post(
        "/ask", json={"question": "What is in the quarterly report?", "top_k": 3}
    )
    assert ask_resp.status_code == 200
    sources = ask_resp.json()["sources"]
    assert "quarterly_report.pdf#page-1" in sources


@pytest.mark.integration
def test_ingest_rejects_empty_or_invalid_payload():
    client = _client()
    assert client.post("/ingest", content=b"").status_code == 400
    assert client.post("/ingest", json={"image_b64": "!!!not-base64!!!"}).status_code == 400


@pytest.mark.integration
def test_ask_returns_answer_field():
    resp = _client().post("/ask", json={"question": "What is Q3 revenue?"})
    assert resp.status_code == 200
    body = resp.json()
    assert "answer" in body and "Q3 revenue" in body["answer"]


@pytest.mark.integration
def test_ask_rejects_invalid_base64():
    resp = _client().post("/ask", json={"question": "Q?", "image_b64": "not_valid_base64!"})
    assert resp.status_code == 400


@pytest.mark.integration
def test_ask_includes_sources_when_retrieved():
    client = _client()
    b64_img = base64.b64encode(b"chart: Q3 revenue is $4.2M").decode("ascii")
    ingest_resp = client.post("/ingest", json={"image_b64": b64_img, "source_id": "chart-q3"})
    assert ingest_resp.status_code == 200

    ask_resp = client.post("/ask", json={"question": "What is Q3 revenue?", "top_k": 2})
    assert ask_resp.status_code == 200
    data = ask_resp.json()
    assert "chart-q3" in data["sources"]


# --- gemini service (unit, offline deterministic + mocked live client) --------
@pytest.mark.unit
def test_split_visual_chunks_validation():
    with pytest.raises(ValueError):
        gemini.split_visual_chunks(b"")
    assert len(gemini.split_visual_chunks(b"%PDF-1.4 single /Type /Page only")) == 1


@pytest.mark.unit
def test_caption_image_returns_text():
    text = gemini.caption_image(b"\x89PNG\r\n\x1a\nchart-data")
    assert isinstance(text, str) and len(text) > 0


@pytest.mark.unit
def test_embed_text_returns_vector_of_expected_dim():
    vec = to_vector("Quarterly revenue growth chart")
    assert isinstance(vec, list)
    assert len(vec) == gemini.DEFAULT_EMBEDDING_DIM
    assert all(isinstance(x, float) for x in vec)


@pytest.mark.unit
def test_answer_uses_image_when_provided():
    ans_without = gemini.answer("Explain trend", ["Revenue grew 18%"], image_bytes=None)
    ans_with = gemini.answer("Explain trend", ["Revenue grew 18%"], image_bytes=b"img-bytes")
    assert ans_with != ans_without
    assert "with image" in ans_with


@pytest.mark.unit
def test_gemini_validation_and_live_sdk_branch(monkeypatch: pytest.MonkeyPatch):
    with pytest.raises(ValueError):
        gemini.caption_image(b"")
    with pytest.raises(ValueError):
        gemini.embed_text("   ")
    with pytest.raises(ValueError):
        gemini.answer("   ", [])

    monkeypatch.setenv("GEMINI_MOCK", "0")
    monkeypatch.setenv("GEMINI_API_KEY", "real-looking-test-key-123")

    class FakeEmbedding:
        values = [0.1, 0.2, 0.3, 0.4]

    class FakeEmbedResponse:
        embeddings = [FakeEmbedding()]

    class FakeGenResponse:
        text = "Mocked live SDK response"

    class FakeModels:
        def generate_content(self, model: str, contents: Any) -> FakeGenResponse:
            return FakeGenResponse()

        def embed_content(self, model: str, contents: Any, config: Any) -> FakeEmbedResponse:
            return FakeEmbedResponse()

    class FakeClient:
        def __init__(self, api_key: str) -> None:
            self.api_key = api_key
            self.models = FakeModels()

    import google.genai as genai_mod

    monkeypatch.setattr(genai_mod, "Client", FakeClient)

    assert gemini.caption_image(b"png-bytes") == "Mocked live SDK response"
    assert gemini.embed_text("hello", dim=4) == [0.1, 0.2, 0.3, 0.4]
    assert gemini.answer("question?", ["ctx"], image_bytes=b"png") == "Mocked live SDK response"


# --- ranking helpers (pure, unit) ---------------------------------------------
@pytest.mark.unit
def test_cosine_identical_vectors_is_one():
    assert cosine_similarity([1, 2, 3], [1, 2, 3]) == pytest.approx(1.0)


@pytest.mark.unit
def test_cosine_orthogonal_is_zero():
    assert cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0)


@pytest.mark.unit
def test_cosine_zero_vector_returns_zero():
    assert cosine_similarity([0, 0], [1, 2]) == 0.0


@pytest.mark.unit
def test_cosine_length_mismatch_raises():
    with pytest.raises(ValueError):
        cosine_similarity([1, 2], [1, 2, 3])


@pytest.mark.unit
def test_rank_returns_top_k():
    cands = [{"id": i, "embedding": [i, 0]} for i in range(1, 6)]
    out = rank_by_similarity([1, 0], cands, k=2)
    assert len(out) == 2


@pytest.mark.unit
def test_rank_orders_most_similar_first():
    cands = [{"id": "a", "embedding": [0, 1]}, {"id": "b", "embedding": [1, 0]}]
    out = rank_by_similarity([1, 0], cands, k=2)
    assert out[0]["id"] == "b" and "score" in out[0]


# --- integration (end-to-end offline ingest -> ask) ---------------------------
@pytest.mark.integration
def test_end_to_end_ingest_then_ask():
    client = _client()
    files = {"file": ("revenue_chart.png", b"\x89PNG\r\n\x1a\nq4-metrics", "image/png")}
    r_ingest = client.post("/ingest", files=files)
    assert r_ingest.status_code == 200
    doc_id = r_ingest.json()["doc_id"]
    assert doc_id == "revenue_chart.png"

    b64_query_img = base64.b64encode(b"annotated-zoom").decode("ascii")
    r_ask = client.post(
        "/ask",
        json={"question": "Summarize the Q4 metrics", "image_b64": b64_query_img, "top_k": 3},
    )
    assert r_ask.status_code == 200
    payload = r_ask.json()
    assert doc_id in payload["sources"]
    assert "Summarize the Q4 metrics" in payload["answer"]


# --- live evaluation suite (`uv run pytest -m live`) --------------------------
@pytest.mark.live
def test_live_gemini_and_atlas_roundtrip():
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key or api_key in {"your-gemini-key", "test-key", "mock"}:
        pytest.skip("Live GEMINI_API_KEY required for -m live evaluation")

    svg_bytes = (
        b'<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100">'
        b"<text x='10' y='50'>Q4 Revenue: $5.1M</text></svg>"
    )
    client = _client()
    r_in = client.post("/ingest", files={"file": ("live_chart.svg", svg_bytes, "image/svg+xml")})
    assert r_in.status_code == 200
    r_ask = client.post("/ask", json={"question": "What was Q4 revenue?", "top_k": 2})
    assert r_ask.status_code == 200
    assert len(r_ask.json()["answer"]) > 0
