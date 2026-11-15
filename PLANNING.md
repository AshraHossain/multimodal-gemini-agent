# PLANNING.md — multimodal-gemini-agent

## What this is

A FastAPI service that ingests visual documents (charts, diagrams, scanned pages) and answers questions about them by combining Google Gemini's multimodal reasoning (`google-genai`) with vector retrieval over a MongoDB Atlas knowledge base. Two primary routes are exposed: `POST /ingest` (caption/extract -> embed -> store) and `POST /ask` (retrieve -> reason -> grounded answer).

Both routes, the Gemini service wrapper, and the Atlas storage/retrieval layer are fully implemented with deterministic offline fallback policies (`GEMINI_MOCK=1`, `ATLAS_MOCK=1`) so the entire 30-test suite passes offline with 95% test coverage.

## Architecture

```text
POST /ingest (multipart file or JSON IngestRequest)
        │
        ▼
  app/routers/ingest.py
        ├── app/services/gemini.caption_image()
        ├── app/services/embedding.to_vector() -> gemini.embed_text()
        └── app/services/atlas.store_document()
        ▼
     MongoDB Atlas (or in-memory fallback store in offline mode)

POST /ask (AskRequest: question + optional image_b64 + top_k)
        │
        ▼
  app/routers/ask.py
        ├── app/services/embedding.to_vector()
        ├── app/services/atlas.search_similar()
        │     ├── live: atlas.vector_search_pipeline() ($vectorSearch)
        │     └── offline: embedding.rank_by_similarity() (pure cosine)
        └── app/services/gemini.answer()
        ▼
     AskResponse { answer, sources }
```

### Module responsibilities

| Module | Path | Purpose | Status |
|---|---|---|---|
| FastAPI app | `app/main.py` | Creates the app, mounts `ingest` and `ask` routers, defines `GET /health`. | Implemented |
| Ingest route | `app/routers/ingest.py` | `POST /ingest` — accepts multipart file or JSON base64 payload, captions, embeds, and stores. | Implemented |
| Ask route | `app/routers/ask.py` | `POST /ask` — embeds question, retrieves top-k context, invokes multimodal Gemini, returns grounded `AskResponse`. | Implemented |
| Gemini service | `app/services/gemini.py` | `caption_image`, `embed_text`, `answer` — wraps `google-genai` SDK with deterministic offline fallback. | Implemented |
| Atlas service | `app/services/atlas.py` | `vector_search_pipeline` (pure), `VECTOR_INDEX_DEFINITION`, `store_document`, `search_similar`. | Implemented |
| Embedding service | `app/services/embedding.py` | `cosine_similarity`, `rank_by_similarity` (pure math) and `to_vector`. | Implemented |
| Schemas | `app/models/schemas.py` | Frozen Pydantic models: `IngestRequest`, `IngestResponse`, `AskRequest`, `AskResponse`. | Implemented |
| Tests | `tests/test_suite.py` | 30 unit and integration tests covering schemas, pipeline builder, ranking math, Gemini/Atlas services, and API routes. | 30 passing, 0 skipped, 95% coverage |
