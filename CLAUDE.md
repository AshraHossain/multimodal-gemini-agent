# CLAUDE.md — Multimodal AI Agent with Gemini

Read [AGENTS.md](AGENTS.md) for the shared project overview, architecture map, and core invariants.

## What this repo is

A Python 3.11+ FastAPI service that ingests visual documents (`POST /ingest`) and answers multimodal questions (`POST /ask`) using Google Gemini (`google-genai`) and MongoDB Atlas Vector Search (`$vectorSearch` on `vector_index`).

## Commands

```bash
uv sync                                                      # setup environment from uv.lock
uv run uvicorn app.main:app --reload                         # run local API server
uv run pytest                                                # offline unit + integration tests (30 pass)
uv run pytest --cov=app --cov-report=term-missing            # verify >=80% coverage (currently 95%)
uv run pytest -m live                                        # live Gemini + Atlas smoke tests
uv run ruff check . && uv run ruff format --check .          # lint & formatting check
```

## Layout

- `app/main.py` — FastAPI app wiring `ingest` and `ask` routers + `GET /health`.
- `app/models/schemas.py` — Frozen Pydantic models: `IngestRequest`, `IngestResponse`, `AskRequest`, `AskResponse`.
- `app/routers/ingest.py` — `POST /ingest` (multipart file or JSON base64 -> caption -> embed -> store).
- `app/routers/ask.py` — `POST /ask` (embed question -> retrieve top-k -> multimodal Gemini answer).
- `app/services/gemini.py` — `caption_image`, `embed_text`, `answer` (`google-genai` + offline deterministic mode).
- `app/services/atlas.py` — `vector_search_pipeline` (pure), `VECTOR_INDEX_DEFINITION`, `store_document`, `search_similar`.
- `app/services/embedding.py` — `cosine_similarity`, `rank_by_similarity` (pure), and `to_vector`.
- `data/sample_chart.svg` — Sample chart asset for local testing.
- `tests/test_suite.py` — Offline unit and integration test suite.

## Repo-Specific Rules

- Keep `app/models/schemas.py` as the sole definition of request/response payloads (`ConfigDict(frozen=True)`).
- Keep `app/routers/` free of direct `google.genai` or `pymongo` imports; delegate all external I/O to `app/services/`.
- Keep `atlas.vector_search_pipeline`, `embedding.cosine_similarity`, and `embedding.rank_by_similarity` pure (no network/DB calls, no similarity math in prompts).
- All default tests in `tests/test_suite.py` must run offline (`GEMINI_MOCK=1`, `ATLAS_MOCK=1`).
- Path-scoped rules live in `.claude/rules/` (mirrored in `.agents/rules/`).
- Repo-specific multi-step procedures live in `.claude/skills/` (linked in `.agents/skills/`).
