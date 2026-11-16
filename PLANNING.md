# PLANNING.md — multimodal-gemini-agent

## What this is

A FastAPI service that ingests visual documents (charts, diagrams, multi-page PDFs) and answers questions about them by combining Google Gemini's multimodal reasoning (`google-genai`) with vector retrieval over a MongoDB Atlas knowledge base.

All routes (`/ingest`, `/ask`, `/health`, `/readyz`), the Gemini service wrapper, the Atlas storage/retrieval layer, production guardrails (`413`/`415`/prompt-injection framing), and the evaluation harness (`app/eval.py`) are fully implemented with deterministic offline fallback policies (`GEMINI_MOCK=1`, `ATLAS_MOCK=1`).

## Architecture

```mermaid
flowchart TB
    subgraph HTTP["FastAPI HTTP Layer (app/main.py, app/routers/)"]
        MW["Middleware: X-Request-ID & X-Process-Time-Ms"]
        ING["POST /ingest (app/routers/ingest.py)\nMIME Allowlist (415) • 10MB Cap (413)"]
        ASK["POST /ask (app/routers/ask.py)\nAskRequest Validation • Base64 Check (400)"]
        HLTH["GET /health & GET /readyz"]
    end

    subgraph Pure["Deterministic Core (Pure Functions)"]
        SPL["gemini.split_visual_chunks()"]
        SAN["gemini.sanitize_untrusted_text()"]
        VSP["atlas.vector_search_pipeline()"]
        RNK["embedding.cosine_similarity() & rank_by_similarity()"]
    end

    subgraph Svc["Service Isolation Layer (app/services/)"]
        GSVC["gemini.py\ncaption_image() • embed_text() • answer()"]
        ASVC["atlas.py\nstore_document() • search_similar()"]
    end

    subgraph Ext["Providers (Live Cloud vs. Offline Mock)"]
        GAPI[("Google Gemini SDK\n(google-genai)")]
        MATL[("MongoDB Atlas\n($vectorSearch)")]
        MEM[("Offline Fallback\n(Feature-Hash + In-Memory Store)")]
    end

    MW --> ING & ASK & HLTH
    ING --> SPL --> GSVC --> SAN
    ING --> ASVC
    ASK --> GSVC & ASVC
    ASVC --> VSP & RNK
    GSVC --> GAPI & MEM
    ASVC --> MATL & MEM
```

### Module responsibilities

| Module | Path | Purpose | Status |
|---|---|---|---|
| FastAPI app & middleware | `app/main.py` | Creates app, attaches `X-Request-ID` & `X-Process-Time-Ms` middleware, exposes `/health` and `/readyz`. | Implemented |
| Evaluation harness | `app/eval.py` | Runs golden multimodal benchmark (`Recall@3`, grounding rate, guardrails, p50/p95 latency) -> `data/eval_report.json`. | Implemented |
| Ingest route | `app/routers/ingest.py` | `POST /ingest` — validates MIME/size, splits multi-page PDFs, captions, embeds, and stores. | Implemented |
| Ask route | `app/routers/ask.py` | `POST /ask` — embeds question, retrieves top-k context, invokes multimodal Gemini, returns grounded `AskResponse`. | Implemented |
| Gemini service | `app/services/gemini.py` | `caption_image`, `embed_text`, `answer`, `split_visual_chunks`, `sanitize_untrusted_text` (`google-genai` + offline policy). | Implemented |
| Atlas service | `app/services/atlas.py` | `vector_search_pipeline` (pure), `VECTOR_INDEX_DEFINITION`, `store_document`, `search_similar`. | Implemented |
| Embedding service | `app/services/embedding.py` | `cosine_similarity`, `rank_by_similarity` (pure math) and `to_vector`. | Implemented |
| Schemas | `app/models/schemas.py` | Frozen Pydantic models: `IngestRequest`, `IngestResponse`, `AskRequest`, `AskResponse`. | Implemented |
| Tests | `tests/test_suite.py` | 36 offline unit/integration tests + 1 `@pytest.mark.live` test. | 36 passing, 93%+ coverage |
