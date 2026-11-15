# TASK.md — multimodal-gemini-agent

Priority task list. See `PLANNING.md` for architecture context.

## Completed

- [x] **Implement `app/services/gemini.py`** — `caption_image`, `embed_text`, `answer`, and `split_visual_chunks` implemented using `google-genai` with deterministic offline policy for tests.
- [x] **Implement `POST /ingest`** (`app/routers/ingest.py`) — supports multipart `UploadFile`, JSON `IngestRequest` (`image_b64`), and multi-page PDF chunking (`#page-N`).
- [x] **Implement `POST /ask`** (`app/routers/ask.py`) — embeds questions, runs `atlas.search_similar`, and invokes `gemini.answer` with retrieved context and optional image.
- [x] **Wire MongoDB client & offline store in `app/services/atlas.py`** — added `VECTOR_INDEX_DEFINITION`, `store_document`, and `search_similar` while keeping `vector_search_pipeline` pure.
- [x] **Unskip all 7 tests & enforce 80%+ coverage** — expanded `tests/test_suite.py` to 32 offline unit/integration tests + 1 `@pytest.mark.live` evaluation test (95% coverage, 0 skipped in offline suite).
- [x] **Add sample chart asset under `data/`** — created `data/sample_chart.svg`.
- [x] **Add CI workflow & Dockerfile** — configured `.github/workflows/ci.yml` and multi-stage `uv`-based `Dockerfile`.
- [x] **Align agent instructions & rules** — added `AGENTS.md`, `GEMINI.md`, concise `CLAUDE.md`, path-scoped `.claude/rules/` (linked to `.agents/rules/`), and repo skills in `.claude/skills/` (linked to `.agents/skills/`).
