"""20-test suite for the Multimodal Gemini Agent.

Tests that exercise pure scaffolding (schemas, the Atlas pipeline builder, the
health route) pass today. Tests that need external services or unimplemented
logic are marked `skip` with a clear reason — unskip them as you implement.
"""
import pytest

from app.models.schemas import AskRequest, AskResponse, IngestResponse
from app.services.atlas import vector_search_pipeline
from app.services.embedding import cosine_similarity, rank_by_similarity


def _client():
    """Build a FastAPI TestClient, skipping if FastAPI isn't installed."""
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app)


# --- schemas (pure, pass now) -------------------------------------------------
def test_ask_request_defaults_top_k():
    assert AskRequest(question="hi").top_k == 4

def test_ask_request_accepts_image():
    assert AskRequest(question="q", image_b64="abc").image_b64 == "abc"

def test_ask_response_sources_default_empty():
    assert AskResponse(answer="a").sources == []

def test_ingest_response_fields():
    r = IngestResponse(doc_id="d1", chunks=3)
    assert r.doc_id == "d1" and r.chunks == 3

def test_ask_request_rejects_missing_question():
    with pytest.raises(Exception):
        AskRequest()


# --- atlas pipeline builder (pure, pass now) ----------------------------------
def test_pipeline_has_vector_search_stage():
    p = vector_search_pipeline([0.1, 0.2], k=4)
    assert p[0].get("$vectorSearch") is not None

def test_pipeline_limit_matches_k():
    p = vector_search_pipeline([0.0], k=7)
    assert p[0]["$vectorSearch"]["limit"] == 7

def test_pipeline_num_candidates_scales_with_k():
    p = vector_search_pipeline([0.0], k=5)
    assert p[0]["$vectorSearch"]["numCandidates"] == 50

def test_pipeline_uses_custom_index_name():
    p = vector_search_pipeline([0.0], index="my_index")
    assert p[0]["$vectorSearch"]["index"] == "my_index"

def test_pipeline_path_is_embedding():
    p = vector_search_pipeline([0.0])
    assert p[0]["$vectorSearch"]["path"] == "embedding"


# --- API routes ---------------------------------------------------------------
def test_health_ok():
    assert _client().get("/health").json() == {"status": "ok"}

def test_health_status_code():
    assert _client().get("/health").status_code == 200

@pytest.mark.skip(reason="implement /ingest")
def test_ingest_returns_doc_id():
    ...

@pytest.mark.skip(reason="implement /ask")
def test_ask_returns_answer_field():
    ...

@pytest.mark.skip(reason="implement /ask grounding")
def test_ask_includes_sources_when_retrieved():
    ...


# --- gemini service (mocked, implement) --------------------------------------
@pytest.mark.skip(reason="implement gemini.caption_image")
def test_caption_image_returns_text():
    ...

@pytest.mark.skip(reason="implement gemini.embed_text")
def test_embed_text_returns_vector_of_expected_dim():
    ...

@pytest.mark.skip(reason="implement gemini.answer multimodal path")
def test_answer_uses_image_when_provided():
    ...


# --- ranking helpers (implemented, pure) -------------------------------------
def test_cosine_identical_vectors_is_one():
    assert cosine_similarity([1, 2, 3], [1, 2, 3]) == pytest.approx(1.0)

def test_cosine_orthogonal_is_zero():
    assert cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0)

def test_cosine_length_mismatch_raises():
    with pytest.raises(ValueError):
        cosine_similarity([1, 2], [1, 2, 3])

def test_rank_returns_top_k():
    cands = [{"id": i, "embedding": [i, 0]} for i in range(1, 6)]
    out = rank_by_similarity([1, 0], cands, k=2)
    assert len(out) == 2

def test_rank_orders_most_similar_first():
    cands = [{"id": "a", "embedding": [0, 1]}, {"id": "b", "embedding": [1, 0]}]
    out = rank_by_similarity([1, 0], cands, k=2)
    assert out[0]["id"] == "b" and "score" in out[0]


# --- integration --------------------------------------------------------------
@pytest.mark.skip(reason="needs Atlas test container")
def test_end_to_end_ingest_then_ask():
    ...
