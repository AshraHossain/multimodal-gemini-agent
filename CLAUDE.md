# CLAUDE.md — Multimodal AI Agent with Gemini

Read [AGENTS.md](AGENTS.md) for the shared project overview, architecture map, and core invariants.

## What this repo is

A Python 3.11+ FastAPI service that ingests visual documents (`POST /ingest`) and answers multimodal questions (`POST /ask`) using Google Gemini (`google-genai`) and MongoDB Atlas Vector Search (`$vectorSearch` on `vector_index`).

## Commands

```bash
make setup                                                   # uv sync
make check                                                   # ruff + pytest (>=80% cov) + evaluation harness
uv run uvicorn app.main:app --reload                         # run local API server
uv run pytest                                                # offline unit + integration tests (36 pass)
uv run pytest --cov=app --cov-report=term-missing            # verify >=80% coverage (currently 93%+)
uv run pytest -m live                                        # live Gemini + Atlas smoke tests
uv run python -m app.eval                                    # run evaluation benchmark -> data/eval_report.json
uv run ruff check . && uv run ruff format --check .          # lint & formatting check
```

## Layout

- `app/main.py` — FastAPI app, `X-Request-ID` & latency middleware, `GET /health`, `GET /readyz`.
- `app/eval.py` — Reproducible multimodal evaluation & latency benchmark runner.
- `app/models/schemas.py` — Frozen Pydantic models: `IngestRequest`, `IngestResponse`, `AskRequest`, `AskResponse`.
- `app/routers/ingest.py` — `POST /ingest` (MIME/size guardrails, multi-page PDF chunking, caption -> embed -> store).
- `app/routers/ask.py` — `POST /ask` (embed question -> retrieve top-k -> multimodal Gemini answer).
- `app/services/gemini.py` — `caption_image`, `embed_text`, `answer`, `sanitize_untrusted_text`, `split_visual_chunks`.
- `app/services/atlas.py` — `vector_search_pipeline` (pure), `VECTOR_INDEX_DEFINITION`, `store_document`, `search_similar`.
- `app/services/embedding.py` — `cosine_similarity`, `rank_by_similarity` (pure), and `to_vector`.
- `data/` — `sample_chart.svg` and `eval_report.json`.
- `tests/test_suite.py` — 36 offline unit/integration tests + 1 `@pytest.mark.live` test.

## Repo-Specific Rules

- Keep `app/models/schemas.py` as the sole definition of request/response payloads (`ConfigDict(frozen=True)`).
- Keep `app/routers/` free of direct `google.genai` or `pymongo` imports; delegate all external I/O to `app/services/`.
- Keep `atlas.vector_search_pipeline`, `embedding.cosine_similarity`, and `embedding.rank_by_similarity` pure (no network/DB calls, no similarity math in prompts).
- All default tests in `tests/test_suite.py` must run offline (`GEMINI_MOCK=1`, `ATLAS_MOCK=1`).
- Path-scoped rules live in `.claude/rules/` (mirrored in `.agents/rules/`).
- Repo-specific multi-step procedures live in `.claude/skills/` (linked in `.agents/skills/`).
