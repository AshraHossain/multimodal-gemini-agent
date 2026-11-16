# AGENTS.md — multimodal-gemini-agent

Portable agent instructions for **Antigravity (Gemini)**, **Claude Code**, and other coding agents working in this repository.

## What this project is

A FastAPI service that ingests visual documents (charts, diagrams, multi-page PDFs) and answers grounded questions over them using **Google Gemini** (`google-genai`, multimodal captioning/reasoning + `text-embedding-004`) and **MongoDB Atlas Vector Search** (`$vectorSearch` on `vector_index`).

When `GEMINI_API_KEY` or `MONGODB_URI` are unconfigured (or `GEMINI_MOCK=1` / `ATLAS_MOCK=1`), the service layer automatically uses deterministic offline policies and an in-memory vector store ranked by pure cosine similarity.

## Verified Commands

```bash
make setup                                                   # uv sync (install locked dependencies)
make check                                                   # ruff lint + pytest (>=80% cov) + eval harness
make dev                                                     # uv run uvicorn app.main:app --reload
uv run pytest                                                # run offline unit + integration tests (36 pass)
uv run pytest --cov=app --cov-report=term-missing            # run suite with coverage gate (93%+ coverage)
uv run pytest -m live                                        # run live Gemini/Atlas tests (requires real .env keys)
uv run python -m app.eval                                    # run golden evaluation & latency benchmark -> data/eval_report.json
uv run ruff check . && uv run ruff format --check .          # lint and format check
```

## Architecture & Layout

```text
app/
  main.py                  # FastAPI entrypoint, telemetry middleware, /health & /readyz
  eval.py                  # Deterministic evaluation & latency benchmark runner
  models/schemas.py        # Frozen Pydantic DTOs: IngestRequest, IngestResponse, AskRequest, AskResponse
  routers/ingest.py        # POST /ingest (MIME/size guardrails, PDF page splitting, caption -> embed -> store)
  routers/ask.py           # POST /ask (question + optional image_b64 -> vector search -> grounded answer)
  services/gemini.py       # Gemini SDK wrapper (caption_image, embed_text, answer, sanitize_untrusted_text, split_visual_chunks)
  services/atlas.py        # Pure vector_search_pipeline builder, VECTOR_INDEX_DEFINITION, store/search
  services/embedding.py    # Pure cosine_similarity, rank_by_similarity, and to_vector delegate
data/
  sample_chart.svg         # Sample chart asset for local ingest/ask smoke tests
  eval_report.json         # Reproducible evaluation scorecard
tests/test_suite.py        # 36 offline unit & integration tests + 1 @pytest.mark.live test
PLANNING.md                # Architecture reference and request flow
SECURITY.md                # Threat model and security controls
TASK.md                    # Tracked backlog and completed milestones
```

## Repo-Specific Rules (Do Not Break)

1. **Single Schema Source**: All HTTP request/response shapes live in `app/models/schemas.py` with `ConfigDict(frozen=True)`. Never accept or return ad-hoc unvalidated dicts in routers.
2. **Thin Routers, Isolated SDKs**: `app/routers/` only validate HTTP/MIME/size/base64 inputs and orchestrate `app/services/` calls. Never import `google.genai` or `pymongo` inside `app/routers/`.
3. **Pure Math & Pipeline Builders Stay Pure**: `atlas.vector_search_pipeline`, `embedding.cosine_similarity`, and `embedding.rank_by_similarity` must remain deterministic and side-effect-free (no network, DB, or env reads, and never compute similarity or rankings inside LLM prompts).
4. **Offline-First Test Suite**: Default `uv run pytest` must pass 100% offline with `GEMINI_MOCK=1` and `ATLAS_MOCK=1`. Live external calls must be marked `@pytest.mark.live`.

## Scoped Rules & Repo Skills

- **Path-scoped rules**: `.agents/rules/` (mirrored to `.claude/rules/`):
  - `routers.md` (`app/routers/**/*.py`)
  - `services.md` (`app/services/**/*.py`)
  - `models-and-tests.md` (`app/models/**/*.py`, `tests/**/*.py`)
- **Repo-specific skills**: `.agents/skills/` (linked to `.claude/skills/`):
  - `add-multimodal-endpoint` — end-to-end TDD procedure for adding/updating multimodal routes and services
  - `atlas-vector-index` — procedure for provisioning and verifying the MongoDB Atlas `vector_index`
