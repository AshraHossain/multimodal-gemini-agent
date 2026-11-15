---
name: atlas-vector-index
description: >-
  Use this skill when provisioning, updating, or verifying the MongoDB Atlas
  Vector Search index (`vector_index`) or testing live Atlas/Gemini connectivity
  in multimodal-gemini-agent.
---

# Configure and Verify MongoDB Atlas Vector Search Index

Follow this runbook to set up the `vector_index` in MongoDB Atlas and verify end-to-end multimodal ingestion and retrieval.

## 1. Inspect the Canonical Index Definition

The canonical Atlas Vector Search index definition lives in `app/services/atlas.py` (`VECTOR_INDEX_DEFINITION`):

```bash
uv run python -c "import json; from app.services.atlas import VECTOR_INDEX_DEFINITION; print(json.dumps(VECTOR_INDEX_DEFINITION, indent=2))"
```

Ensure `numDimensions` matches the configured embedding dimensionality (`768` for `text-embedding-004` in production, or `DEFAULT_EMBEDDING_DIM` in local overrides) and `similarity` is set to `"cosine"`.

## 2. Verify Pipeline Generation Offline

Verify that `vector_search_pipeline` produces the expected `$vectorSearch` stage:

```bash
uv run pytest tests/test_suite.py -k "pipeline or atlas" -v
```

## 3. Configure `.env` for Live Connectivity

Copy `.env.example` to `.env` and populate:
- `GEMINI_API_KEY` — valid Google AI Studio / Gemini API key
- `MONGODB_URI` — `mongodb+srv://...` connection string
- `MONGODB_DB=multimodal`
- `VECTOR_INDEX=vector_index`
- `GEMINI_MODEL=gemini-2.5-flash`

## 4. Smoke Test `/ingest` and `/ask` with Sample Asset

Start the server and ingest `data/sample_chart.svg`:

```bash
uv run uvicorn app.main:app --port 8000 &
SERVER_PID=$!
sleep 2
curl -sS -X POST http://127.0.0.1:8000/ingest -F "file=@data/sample_chart.svg;type=image/svg+xml"
curl -sS -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question": "What are the quarterly revenue values?", "top_k": 3}'
kill $SERVER_PID
```
