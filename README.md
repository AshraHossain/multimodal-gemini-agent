# Multimodal AI Agent with Gemini

An agent that ingests visual documents — charts, diagrams, scanned pages — and answers questions by combining Google Gemini's multimodal reasoning (`google-genai`) with vector retrieval over a MongoDB Atlas knowledge base (`$vectorSearch`).

## Stack

- **Model:** Google Gemini (`gemini-2.5-flash` / `gemini-2.5-pro`) via `google-genai` for native image + text reasoning
- **Vector store:** MongoDB Atlas Vector Search (`$vectorSearch` on `vector_index`) with an automatic offline in-memory fallback
- **Embeddings:** Gemini `text-embedding-004`
- **API:** FastAPI (async) with `POST /ingest`, `POST /ask`, and `GET /health`

## Architecture

```text
upload (image/PDF page) ──► Gemini caption + extract ──► embed ──► MongoDB Atlas Vector
                                                                        │
question + (optional image) ──► retrieve context ──► Gemini multimodal ──► grounded answer
```

## Getting Started

Dependency management is [UV](https://docs.astral.sh/uv/)-based:

```bash
uv sync
cp .env.example .env   # set GEMINI_API_KEY + MONGODB_URI for live mode
uv run uvicorn app.main:app --reload
uv run pytest --cov=app --cov-report=term-missing   # 30 pass offline (95% coverage)
uv run ruff check .
```

## Project Layout

```text
app/
  main.py              # FastAPI app + routes
  routers/             # ingest + ask endpoints
  services/            # gemini client, atlas vector search, embedding helpers
  models/              # frozen pydantic request/response schemas
data/
  sample_chart.svg     # sample chart for smoke testing
tests/
  test_suite.py        # 30 offline unit + integration tests
.agents/               # Antigravity rules + skills links
.claude/               # Path-scoped rules + repo-specific skills
```

## Atlas Setup

Create a vector search index named `vector_index` on the `embedding` field (`cosine` similarity). See `VECTOR_INDEX_DEFINITION` in [atlas.py](app/services/atlas.py) or run the `atlas-vector-index` skill in `.agents/skills/atlas-vector-index/SKILL.md`.
