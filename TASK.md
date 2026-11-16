# TASK.md — multimodal-gemini-agent

Priority task list. See [PLANNING.md](PLANNING.md) for architecture context.

## Completed

- [x] **Implement `app/services/gemini.py`** — `caption_image`, `embed_text`, `answer`, `split_visual_chunks`, and `sanitize_untrusted_text` implemented using `google-genai` with deterministic feature-hashed offline policy.
- [x] **Implement `POST /ingest`** (`app/routers/ingest.py`) — supports multipart `UploadFile`, JSON `IngestRequest` (`image_b64`), multi-page PDF chunking (`#page-N`), MIME allowlist (`415`), and `10 MB` size cap (`413`).
- [x] **Implement `POST /ask`** (`app/routers/ask.py`) — embeds questions, runs `atlas.search_similar`, and invokes `gemini.answer` with `<untrusted_context>` prompt-injection framing and optional query-time image.
- [x] **Wire MongoDB client & offline store in `app/services/atlas.py`** — added `VECTOR_INDEX_DEFINITION`, `store_document`, and `search_similar` while keeping `vector_search_pipeline` pure.
- [x] **Add telemetry middleware & readiness probe** (`app/main.py`) — `X-Request-ID`, `X-Process-Time-Ms`, `/health`, and `/readyz`.
- [x] **Add reproducible evaluation & benchmark harness** (`app/eval.py`) — computes `Recall@3`, citation grounding rate, guardrail pass rate, and p50/p95 latency into `data/eval_report.json`.
- [x] **Unskip all tests & enforce 80%+ coverage** — 36 passing offline unit/integration tests + 1 `@pytest.mark.live` test (93%+ coverage).
- [x] **Add CI workflow, `Dockerfile`, `docker-compose.yml`, `Makefile`, and `SECURITY.md`** — full containerization and automated quality gate.
- [x] **Align agent instructions & rules** — added `AGENTS.md`, `GEMINI.md`, concise `CLAUDE.md`, path-scoped `.claude/rules/` (linked to `.agents/rules/`), and repo skills in `.claude/skills/` (linked to `.agents/skills/`).
