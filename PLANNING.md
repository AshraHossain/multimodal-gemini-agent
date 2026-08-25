# PLANNING.md — multimodal-gemini-agent

## What this is

A FastAPI service that ingests visual documents (charts, diagrams, scanned
pages) and answers questions about them by combining Google Gemini's
multimodal reasoning with vector retrieval over a MongoDB Atlas knowledge
base. Two routes are planned: `POST /ingest` (caption/extract → embed →
store) and `POST /ask` (retrieve → reason → grounded answer).

This is an early-stage scaffold, not a working system yet: the FastAPI app,
routers, and Pydantic schemas are wired up and tested, but both routes and
every Gemini service function currently `raise NotImplementedError`. The
Atlas pipeline builder and the local cosine-similarity ranking helpers are
fully implemented and unit-tested — see "What's actually implemented" below.

## Architecture

```
POST /ingest (image/PDF page)
        │
        ▼
  app/routers/ingest.py     -- NotImplementedError (stub)
        │  (planned) calls app/services/gemini.caption_image
        │  (planned) calls app/services/embedding.to_vector -> gemini.embed_text
        │  (planned) stores document + embedding in MongoDB Atlas
        ▼
     MongoDB Atlas (single store: documents + vector index "vector_index")

POST /ask (question + optional image)
        │
        ▼
  app/routers/ask.py        -- NotImplementedError (stub)
        │  (planned) app/services/atlas.vector_search_pipeline() -- IMPLEMENTED
        │  (planned) app/services/embedding.rank_by_similarity() -- IMPLEMENTED (local fallback)
        │  (planned) app/services/gemini.answer() -- NotImplementedError
        ▼
     AskResponse { answer, sources }
```

### Module responsibilities

| Module | Path | Purpose | Status |
|---|---|---|---|
| FastAPI app | `app/main.py` | Creates the app, includes `ingest` and `ask` routers, defines `GET /health`. | Working |
| Ingest route | `app/routers/ingest.py` | `POST /ingest` — accept an image/PDF page, caption + embed + store. | Stub — `raise NotImplementedError` |
| Ask route | `app/routers/ask.py` | `POST /ask` — accept a question (+ optional image), retrieve, call Gemini, return a grounded answer. | Stub — `raise NotImplementedError` |
| Gemini service | `app/services/gemini.py` | `caption_image`, `embed_text`, `answer` — wraps the Gemini SDK for multimodal reasoning and embeddings. | Stub — all three `raise NotImplementedError` |
| Atlas service | `app/services/atlas.py` | `vector_search_pipeline(vector, k, index)` — builds a MongoDB `$vectorSearch` aggregation stage. | **Implemented**, unit-tested |
| Embedding service | `app/services/embedding.py` | `cosine_similarity`, `rank_by_similarity` (pure, local ranking) and `to_vector` (delegates to `gemini.embed_text`). | Ranking helpers **implemented**; `to_vector` depends on the still-stubbed Gemini service |
| Schemas | `app/models/schemas.py` | Pydantic models: `IngestResponse`, `AskRequest`, `AskResponse`. | Working |
| Tests | `tests/test_suite.py` | 24 tests (the file's own docstring says "20-test suite," which is stale): schema validation, Atlas pipeline builder, health route, and ranking helpers pass today; route/Gemini-service tests are `@pytest.mark.skip`'d with a reason until implemented. | 17 passing, 7 skipped (by design), verified via `uv run pytest` |

### Request flow (as designed, once implemented)

1. `POST /ingest` receives an image/PDF page → `gemini.caption_image` extracts
   text → `embedding.to_vector` (via `gemini.embed_text`) embeds it → the
   document + embedding are stored in MongoDB Atlas.
2. `POST /ask` receives a question (+ optional image) → the question is
   embedded → `atlas.vector_search_pipeline` builds the `$vectorSearch`
   aggregation to retrieve the top-`k` matching documents from Atlas →
   `gemini.answer` reasons over the question, retrieved context, and any
   attached image → `AskResponse { answer, sources }` is returned.
3. `rank_by_similarity` in `embedding.py` exists as a pure local fallback
   ranker (cosine similarity, no external dependency) for cases where
   candidates are already in memory rather than re-querying Atlas.

### External dependencies

- **Google Gemini API** — `GEMINI_API_KEY` (`.env.example`). Model configured
  via `GEMINI_MODEL` (default `gemini-1.5-pro`). Used for both multimodal
  reasoning (`gemini.answer`) and text embeddings (`gemini.embed_text`).
- **MongoDB Atlas** — `MONGODB_URI`, `MONGODB_DB` (`.env.example`). Also
  serves as the vector index (`VECTOR_INDEX`, default `vector_index`) via the
  `$vectorSearch` aggregation stage — one database for both document store
  and vector search, no separate vector DB.

## Key design constraints

- **Both routes are unimplemented stubs** — `POST /ingest` and `POST /ask`
  both `raise NotImplementedError`. Implementing them is the primary
  next step; see `TASK.md`.
- **Gemini service is fully stubbed** — `caption_image`, `embed_text`, and
  `answer` in `app/services/gemini.py` all `raise NotImplementedError`.
  `embedding.to_vector` depends on `gemini.embed_text` and will fail until
  that's implemented.
- **Atlas pipeline builder is pure and complete** — `vector_search_pipeline`
  has no external dependency (it returns a plain aggregation-pipeline list)
  and is fully covered by tests; it does not itself execute a query against
  Atlas — that wiring (an actual Mongo client + `.aggregate()` call) does not
  exist yet.
- **No `data/` sample assets** — the README references a `data/` directory
  for sample charts/diagrams used in the quickstart; it is not present in
  the repo yet.
- **No live model/DB calls in tests** — the 17 passing tests exercise pure
  logic (schemas, pipeline builder, ranking math) and the `/health` route
  only; none of them touch the real Gemini API or a real Atlas cluster.

## Next steps (not yet done)

1. Implement `app/services/gemini.py`: `caption_image`, `embed_text`,
   `answer` (multimodal, using `GEMINI_MODEL`).
2. Implement `app/routers/ingest.py`: wire caption → embed → store in Atlas.
3. Implement `app/routers/ask.py`: embed question → `vector_search_pipeline`
   → retrieve from Atlas → `gemini.answer` → `AskResponse`.
4. Add the actual MongoDB client/connection wiring in `app/services/atlas.py`
   (currently only the pipeline builder exists — no `.aggregate()` call).
5. Unskip the corresponding tests in `tests/test_suite.py` as each piece
   lands (currently 7 tests are skipped pending implementation).
6. Add sample chart/diagram assets under `data/` to match the README
   quickstart instructions.
