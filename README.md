# Multimodal AI Agent with Gemini & MongoDB Atlas

[![CI](https://github.com/AshraHossain/multimodal-gemini-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/AshraHossain/multimodal-gemini-agent/actions)
![Coverage](https://img.shields.io/badge/coverage-99.7%25-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash%20%7C%20Pro-4F46E5)
![MongoDB Atlas](https://img.shields.io/badge/MongoDB%20Atlas-%24vectorSearch-10B981)

An enterprise-grade FastAPI service that ingests visual documents — charts, architecture diagrams, and multi-page PDFs — and answers grounded questions over them by combining **Google Gemini** (`google-genai`, multimodal captioning/reasoning + `text-embedding-004`) with **MongoDB Atlas Vector Search** (`$vectorSearch` on `vector_index`).

---

## Key Enterprise Capabilities

- **Multimodal Ingestion & Multi-Page PDF Chunking (`POST /ingest`)**: Accepts multipart file uploads or base64 JSON payloads (`IngestRequest`), automatically splits multi-page PDFs into per-page visual chunks (`#page-1`, `#page-2`, ...), extracts structured captions via Gemini, embeds them, and indexes into MongoDB Atlas.
- **Grounded Multimodal Q&A (`POST /ask`)**: Embeds the user's question, executes a `$vectorSearch` aggregation pipeline (or pure cosine-similarity fallback in offline mode), frames untrusted context inside `<untrusted_context>` prompt-injection boundaries, and reasons multimodally over retrieved evidence + optional query-time images.
- **Production Guardrails & Telemetry**:
  - `X-Request-ID` correlation and `X-Process-Time-Ms` latency telemetry middleware on all endpoints.
  - Strict MIME-type allowlist (`HTTP 415`) and `10 MB` payload ceiling (`HTTP 413`).
  - Liveness (`GET /health`) and readiness (`GET /readyz`) probes.
- **100% Offline-Testable & Reproducible Evaluation Suite**: Automatic deterministic fallback (`GEMINI_MOCK=1`, `ATLAS_MOCK=1`) with **96% test coverage** and an executable benchmark harness (`uv run python -m app.eval`).

---

## System Architecture & Request Flow

### 1. Layered System Architecture

```mermaid
flowchart LR
    subgraph Client["Client & CI Surface"]
        U["REST Client / curl"]
        EV["Evaluation Harness\n(app/eval.py)"]
    end

    subgraph Edge["FastAPI Edge & Guardrails (app/main.py)"]
        MW["Telemetry & Correlation\n(X-Request-ID, X-Process-Time-Ms)"]
        PR["Liveness & Readiness\n(GET /health, GET /readyz)"]
    end

    subgraph Routers["Thin HTTP Router Boundary (app/routers/)"]
        IN["POST /ingest\n• MIME Allowlist (415)\n• 10 MB Cap (413)"]
        ASK["POST /ask\n• Base64 Validation (400)\n• Frozen AskRequest DTO"]
    end

    subgraph Core["Deterministic Pure Core (Side-Effect Free)"]
        SPLIT["split_visual_chunks()\n(Multi-page PDF Splitter)"]
        SAN["sanitize_untrusted_text()\n(<untrusted_context> Framing)"]
        PIPE["vector_search_pipeline()\n($vectorSearch Stage Builder)"]
        MATH["cosine_similarity() &\nrank_by_similarity()"]
    end

    subgraph Services["Isolated Service Adapters (app/services/)"]
        GEM["gemini.py\ncaption_image | embed_text | answer"]
        ATL["atlas.py\nstore_document | search_similar"]
    end

    subgraph Backends["External Cloud / Offline Fallback"]
        GCLOUD[("Google Gemini API\n(google-genai: 2.5-flash +\ntext-embedding-004)")]
        MDB[("MongoDB Atlas\n(vector_index)")]
        MOCK[("Deterministic Offline Mode\n(Feature-Hash Vectors +\nIn-Memory Cosine Store)")]
    end

    U --> MW
    EV --> MW
    MW --> PR
    MW --> IN
    MW --> ASK

    IN --> SPLIT
    SPLIT --> GEM
    GEM --> SAN
    IN --> ATL

    ASK --> GEM
    ASK --> ATL
    ATL --> PIPE
    ATL --> MATH

    GEM -. "Live Mode" .-> GCLOUD
    ATL -. "Live Mode" .-> MDB
    GEM -. "GEMINI_MOCK=1" .-> MOCK
    ATL -. "ATLAS_MOCK=1" .-> MOCK
```

### 2. End-to-End Request Sequence

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant API as FastAPI Router (ingest / ask)
    participant Gem as Gemini Service (google-genai)
    participant Emb as Embedding Service (Pure Math)
    participant Atlas as MongoDB Atlas ($vectorSearch)

    rect rgb(240, 248, 255)
    Note over Client,Atlas: Ingestion Flow (POST /ingest)
    Client->>API: Upload Image / Multi-page PDF (<=10MB)
    API->>Gem: split_visual_chunks() + caption_image()
    Gem-->>API: Sanitized visual summary per page
    API->>Emb: to_vector(caption) -> gemini.embed_text()
    Emb-->>API: 768-d float vector
    API->>Atlas: store_document(doc_id, text, embedding, metadata)
    API-->>Client: IngestResponse { doc_id, chunks } + X-Request-ID
    end

    rect rgb(245, 255, 245)
    Note over Client,Atlas: Grounded Q&A Flow (POST /ask)
    Client->>API: AskRequest { question, image_b64?, top_k }
    API->>Emb: to_vector(question)
    API->>Atlas: search_similar(query_vector, k=top_k)
    Atlas-->>API: Top-k matching visual document chunks
    API->>Gem: answer(question, <untrusted_context>, image_bytes)
    Gem-->>API: Grounded response
    API-->>Client: AskResponse { answer, sources } + X-Process-Time-Ms
    end
```

---

## Quickstart

Dependency management is [UV](https://docs.astral.sh/uv/)-based:

```bash
make setup                           # uv sync
cp .env.example .env                 # set GEMINI_API_KEY + MONGODB_URI for live mode
make check                           # ruff lint + pytest (96% coverage) + evaluation harness
make dev                             # uv run uvicorn app.main:app --reload
```

### Smoke Test (`curl`)

```bash
# 1. Readiness probe
curl -i http://127.0.0.1:8000/readyz

# 2. Ingest sample SVG chart
curl -sS -X POST http://127.0.0.1:8000/ingest \
  -F "file=@data/sample_chart.svg;type=image/svg+xml"

# 3. Ask a grounded question
curl -sS -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the quarterly revenue values?", "top_k": 3}'
```

---

## Evaluation & Benchmark Scorecard (`make eval`)

Run `uv run python -m app.eval` to execute the golden multimodal benchmark and write [data/eval_report.json](data/eval_report.json):

| Case ID | Asset Type | Chunks OK | Recall@3 | Citation Grounded |
|---|---|---|---|---|
| `EVAL-01-SVG-CHART` | `image/svg+xml` | `True` (1) | `True` | `True` |
| `EVAL-02-PNG-DIAGRAM` | `image/png` | `True` (1) | `True` | `True` |
| `EVAL-03-MULTIPAGE-PDF` | `application/pdf` (3 pages) | `True` (3) | `True` | `True` |

- **Recall@3**: `100.0%`
- **Citation Grounding Rate**: `100.0%`
- **Security Guardrail Pass Rate (`415` / `400` / Injection Framing)**: `100.0%`

---

## Project Layout

```text
app/
  main.py              # FastAPI app, telemetry middleware, /health & /readyz
  eval.py              # Reproducible multimodal evaluation & benchmark runner
  routers/             # POST /ingest (MIME/size guardrails, PDF splitting) & POST /ask
  services/            # Gemini SDK wrapper, Atlas $vectorSearch builder, pure cosine math
  models/              # Frozen Pydantic DTOs (IngestRequest, IngestResponse, AskRequest, AskResponse)
data/
  sample_chart.svg     # Sample chart asset for smoke testing
  eval_report.json     # Generated evaluation scorecard
tests/
  test_suite.py        # Offline unit + integration suite (96% coverage) + @pytest.mark.live
.agents/               # Antigravity rules + skills links
.claude/               # Path-scoped rules + repo-specific skills
```

## Documentation & Governance

- [AGENTS.md](AGENTS.md) & [GEMINI.md](GEMINI.md) — Agent instructions, scoped rules, and skills
- [PLANNING.md](PLANNING.md) — Detailed module architecture and data flow
- [SECURITY.md](SECURITY.md) — Threat model and security controls
- [CONTRIBUTING.md](CONTRIBUTING.md) — TDD workflow and contribution standards
