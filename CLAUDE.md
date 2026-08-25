# CLAUDE.md — Multimodal AI Agent with Gemini

## What we're building
An agent that understands visual documents (charts, diagrams, scanned pages) and answers questions about them. Visual content is captioned/extracted by Gemini, embedded, and stored in MongoDB Atlas Vector Search. At query time we retrieve relevant context and let Gemini reason multimodally over the question plus any attached image.

## Stack & conventions
- Python 3.11+, FastAPI (async). Google Gemini for multimodal reasoning + embeddings. MongoDB Atlas Vector Search as the single store.
- Pydantic models for all request/response bodies (`app/models/`).
- Service layer (`app/services/`) isolates external SDKs (Gemini, Mongo) so routers stay thin.
- Secrets in `.env`: `GEMINI_API_KEY`, `MONGODB_URI`. Atlas vector index name: `vector_index`.

## Architecture map
- `app/main.py` — FastAPI app, includes routers, health check.
- `app/routers/ingest.py` — accept image/PDF page, caption + embed + store.
- `app/routers/ask.py` — accept question (+ optional image), retrieve, call Gemini, return grounded answer.
- `app/services/gemini.py` — multimodal generate + embeddings wrapper.
- `app/services/atlas.py` — `$vectorSearch` aggregation + index definition snippet.
- `app/services/embedding.py` — text/image → vector.
- `app/models/` — `IngestRequest`, `AskRequest`, `AskResponse`.

## Next concrete steps
1. Define pydantic schemas, then `services/atlas.py` connection + vector search query.
2. Implement `services/gemini.py` (caption an image, embed text, multimodal answer).
3. Wire `/ingest` then `/ask`; test with a sample chart in `data/`.
4. Document the Atlas index creation in README; add a startup check that the index exists.

## Definition of done
`POST /ingest` stores a chart's content; `POST /ask` with a related question returns a Gemini answer grounded in retrieved context, served via `uvicorn app.main:app`.

## Testing
24 tests in `tests/` (the docstring there says "20-test suite" — stale, verified 24 via `pytest --collect-only`) covering schema validation, the Atlas query builder, the embedding shape, the Gemini service interface (mocked), and route behavior. Run with `pytest`. 17 pass today (pure schema/pipeline/ranking logic + `/health`); 7 are `@pytest.mark.skip`'d pending implementation of `/ingest`, `/ask`, and `app/services/gemini.py`.

## Framework conventions

This repo follows the SuperClaude Framework structure:

- **`PLANNING.md`** — architecture reference: module map, request flow,
  what's implemented vs. stubbed, and known constraints. Read this before
  touching `app/`.
- **`TASK.md`** — prioritized backlog (High/Medium/Low). Check here before
  starting work — the stubbed routes and Gemini service functions are
  already tracked, not new discoveries.
- **`plugins/README.md`** — plugin extension point placeholder; no plugin
  system exists yet, `app/services/` calls Gemini/Atlas directly instead.
- Dependency management is **UV-based** (`pyproject.toml` + `uv.lock`) —
  prefer `uv sync` / `uv run`, though `requirements.txt` is kept in sync
  for tooling that expects it.

## Commands

```bash
uv sync                                          # setup
uv run uvicorn app.main:app --reload             # run locally
uv run pytest                                    # tests (17 pass, 7 skipped pending implementation)
```
