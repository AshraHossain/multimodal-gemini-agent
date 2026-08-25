# Project 3 — Multimodal AI Agent with Gemini

An agent that ingests visual documents — charts, diagrams, scanned pages — and answers questions by combining Gemini's multimodal reasoning with vector retrieval over a MongoDB Atlas knowledge base.

## Stack

- **Model:** Google Gemini (`gemini-1.5-pro` / `gemini-2.0-flash`) for native image + text reasoning
- **Vector store:** MongoDB Atlas Vector Search
- **Embeddings:** Gemini `text-embedding-004` (text) + image captions for indexing
- **API:** FastAPI (async) with `/ingest` and `/ask` endpoints
- **Pattern:** tool-calling loop (retrieve → reason → optionally re-retrieve)

## Architecture

```
upload (image/PDF page) ──► Gemini caption + extract ──► embed ──► MongoDB Atlas Vector
                                                                        │
question + (optional image) ──► retrieve context ──► Gemini multimodal ──► grounded answer
```

MongoDB Atlas is both the document store and the vector index (one database, `$vectorSearch` aggregation stage).

## Getting Started

Dependency management is [UV](https://docs.astral.sh/uv/)-based:

```bash
uv sync
cp .env.example .env   # GEMINI_API_KEY + MONGODB_URI
uv run uvicorn app.main:app --reload
uv run pytest          # 17 pass today; 7 skipped pending /ingest, /ask, gemini.py
# POST an image to /ingest, then ask via /ask
```

`requirements.txt` is kept in sync for `pip install -r requirements.txt`
workflows, but `uv sync` (with `pyproject.toml` + `uv.lock`) is the source
of truth for the resolved environment.

**Status:** early-stage scaffold — `/ingest`, `/ask`, and all of
`app/services/gemini.py` currently raise `NotImplementedError`. See
[PLANNING.md](PLANNING.md) for what's implemented vs. stubbed, and
[TASK.md](TASK.md) for the prioritized backlog.

## Project layout

```
app/
  main.py            # FastAPI app + routes
  routers/           # ingest + ask endpoints
  services/          # gemini client, atlas vector search, embedding
  models/            # pydantic request/response schemas
data/                # sample charts/diagrams
```

## Atlas setup
Create a vector search index named `vector_index` on the `embedding` field (dimensions matching the embedding model, cosine similarity). See `app/services/atlas.py` for the index definition snippet.

## Notes
This is the "managed cloud, multimodal" project — contrasts with the local stack of Project 2 and the agent-framework stack of Projects 1 & 4.

## Framework

This repo follows the SuperClaude Framework structure used across this
portfolio — see [PLANNING.md](PLANNING.md) for architecture (including
what's implemented vs. stubbed) and [TASK.md](TASK.md) for the prioritized
backlog. `plugins/README.md` is the reserved extension point for future
Gemini/Atlas plugin integrations. See [CONTRIBUTING.md](CONTRIBUTING.md)
for the full development setup.
