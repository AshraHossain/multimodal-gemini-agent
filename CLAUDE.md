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
20 tests in `tests/` covering schema validation, the Atlas query builder, the embedding shape, the Gemini service interface (mocked), and route behavior. Run with `pytest`.
