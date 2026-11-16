"""Deterministic evaluation & latency benchmark harness for multimodal-gemini-agent.

Run via:
    uv run python -m app.eval
"""
from __future__ import annotations

import base64
import json
import os
import statistics
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

from app.main import app
from app.services import atlas


@dataclass(frozen=True)
class EvalCase:
    """Immutable specification of a single multimodal ingest + ask benchmark case."""

    case_id: str
    doc_id: str
    mime_type: str
    payload: bytes
    question: str
    expected_chunks: int
    expected_source: str


GOLDEN_CASES: tuple[EvalCase, ...] = (
    EvalCase(
        case_id="EVAL-01-SVG-CHART",
        doc_id="q3_revenue_chart.svg",
        mime_type="image/svg+xml",
        payload=b"<svg><text>Q3 Revenue: $4.2M (+27% YoY)</text></svg>",
        question="What was the Q3 revenue?",
        expected_chunks=1,
        expected_source="q3_revenue_chart.svg",
    ),
    EvalCase(
        case_id="EVAL-02-PNG-DIAGRAM",
        doc_id="system_topology.png",
        mime_type="image/png",
        payload=b"\x89PNG\r\n\x1a\n<diagram: API Gateway -> FastAPI -> Atlas Vector Search>",
        question="How does the API Gateway route requests?",
        expected_chunks=1,
        expected_source="system_topology.png",
    ),
    EvalCase(
        case_id="EVAL-03-MULTIPAGE-PDF",
        doc_id="board_deck.pdf",
        mime_type="application/pdf",
        payload=(
            b"%PDF-1.7\n"
            b"1 0 obj << /Type /Page /Contents (Page 1: ARR $18M) >> endobj\n"
            b"2 0 obj << /Type /Page /Contents (Page 2: NRR 124%) >> endobj\n"
            b"3 0 obj << /Type /Page /Contents (Page 3: Gross Margin 81%) >> endobj\n"
        ),
        question="Summarize the board deck metrics",
        expected_chunks=3,
        expected_source="board_deck.pdf#page-1",
    ),
)


def run_evaluation(output_path: Path | None = None) -> dict[str, Any]:
    """Execute the offline golden evaluation suite and return a structured scorecard."""
    os.environ["GEMINI_MOCK"] = "1"
    os.environ["ATLAS_MOCK"] = "1"
    atlas.reset_memory_store()

    client = TestClient(app)
    latencies_ms: list[float] = []
    case_results: list[dict[str, Any]] = []
    recall_hits = 0
    grounding_hits = 0

    for case in GOLDEN_CASES:
        t0 = time.perf_counter()
        b64 = base64.b64encode(case.payload).decode("ascii")
        in_resp = client.post(
            "/ingest",
            json={
                "image_b64": b64,
                "source_id": case.doc_id,
                "mime_type": case.mime_type,
            },
        )
        ask_resp = client.post("/ask", json={"question": case.question, "top_k": 3})
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        latencies_ms.append(elapsed_ms)

        in_body = in_resp.json()
        ask_body = ask_resp.json()
        chunks_ok = in_resp.status_code == 200 and in_body.get("chunks") == case.expected_chunks
        source_recalled = case.expected_source in ask_body.get("sources", [])
        grounded = (
            case.question in ask_body.get("answer", "")
            and len(ask_body.get("sources", [])) > 0
        )

        if source_recalled:
            recall_hits += 1
        if grounded:
            grounding_hits += 1

        case_results.append(
            {
                "case_id": case.case_id,
                "chunks_ok": chunks_ok,
                "recall_at_3": source_recalled,
                "grounded": grounded,
                "latency_ms": round(elapsed_ms, 2),
            }
        )

    # Guardrail verification: 415 Unsupported Media Type + 400 Invalid Base64
    r_415 = client.post(
        "/ingest",
        json={
            "image_b64": base64.b64encode(b"exe").decode("ascii"),
            "mime_type": "application/x-msdownload",
        },
    )
    r_400 = client.post("/ask", json={"question": "Test", "image_b64": "!!!invalid!!!"})
    guardrails_passed = r_415.status_code == 415 and r_400.status_code == 400

    total = len(GOLDEN_CASES)
    sorted_lat = sorted(latencies_ms)
    scorecard: dict[str, Any] = {
        "total_cases": total,
        "recall_at_3": round(recall_hits / total, 4),
        "citation_grounding_rate": round(grounding_hits / total, 4),
        "guardrail_pass_rate": 1.0 if guardrails_passed else 0.0,
        "latency_p50_ms": round(statistics.median(sorted_lat), 2),
        "latency_p95_ms": round(sorted_lat[-1], 2),
        "cases": case_results,
    }

    target_path = output_path or Path("data/eval_report.json")
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(json.dumps(scorecard, indent=2) + "\n", encoding="utf-8")
    return scorecard


def main() -> None:
    scorecard = run_evaluation()
    p50 = scorecard["latency_p50_ms"]
    p95 = scorecard["latency_p95_ms"]
    print("# Multimodal Gemini Agent — Evaluation Scorecard\n")
    print(f"- **Recall@3**: {scorecard['recall_at_3'] * 100:.1f}%")
    print(f"- **Citation Grounding Rate**: {scorecard['citation_grounding_rate'] * 100:.1f}%")
    print(f"- **Guardrail Pass Rate**: {scorecard['guardrail_pass_rate'] * 100:.1f}%")
    print(f"- **Latency (p50 / p95)**: {p50} ms / {p95} ms\n")
    print("| Case ID | Chunks OK | Recall@3 | Grounded | Latency (ms) |")
    print("|---|---|---|---|---|")
    for c in scorecard["cases"]:
        print(
            f"| `{c['case_id']}` | {c['chunks_ok']} | {c['recall_at_3']} | "
            f"{c['grounded']} | {c['latency_ms']} |"
        )


if __name__ == "__main__":
    main()
