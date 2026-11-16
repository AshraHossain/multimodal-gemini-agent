# Graph Report - multimodal-gemini-agent  (2026-11-15)

## Corpus Check
- Corpus is ~7,253 words - fits in a single context window. You may not need a graph.

## Summary
- 154 nodes · 292 edges · 14 communities (8 shown, 2 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Agent Instructions & Rules
- FastAPI Multimodal Routers
- Evaluation & Benchmark Harness
- Agent Instructions & Rules
- Evaluation & Benchmark Harness
- MongoDB Atlas Vector Search
- FastAPI Multimodal Routers
- Agent Instructions & Rules
- Test Suite & Verification (12)
- Agent Instructions & Rules

## God Nodes (most connected - your core abstractions)
1. `ingest()` - 15 edges
2. `_client()` - 14 edges
3. `vector_search_pipeline()` - 12 edges
4. `AskRequest` - 11 edges
5. `ask()` - 10 edges
6. `run_evaluation()` - 9 edges
7. `test_gemini_validation_and_live_sdk_branch()` - 9 edges
8. `search_similar()` - 8 edges
9. `rank_by_similarity()` - 8 edges
10. `caption_image()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Models & Tests Rules (.claude/rules/models-and-tests.md)` --rationale_for--> `AskRequest`  [EXTRACTED]
  /Users/ashraf-macbookair/projects/multimodal-gemini-agent/.claude/rules/models-and-tests.md → app/models/schemas.py
- `SECURITY.md Threat Model` --rationale_for--> `ingest()`  [EXTRACTED]
  SECURITY.md → app/routers/ingest.py
- `Service Layer Rules (.claude/rules/services.md)` --rationale_for--> `vector_search_pipeline()`  [EXTRACTED]
  /Users/ashraf-macbookair/projects/multimodal-gemini-agent/.claude/rules/services.md → app/services/atlas.py
- `Skill: atlas-vector-index` --references--> `vector_search_pipeline()`  [EXTRACTED]
  /Users/ashraf-macbookair/projects/multimodal-gemini-agent/.claude/skills/atlas-vector-index/SKILL.md → app/services/atlas.py
- `SECURITY.md Threat Model` --rationale_for--> `sanitize_untrusted_text()`  [EXTRACTED]
  SECURITY.md → app/services/gemini.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Ask Pipeline: Embed -> Search Similar -> Multimodal Answer** — app_routers_ask_ask, app_services_embedding_to_vector, app_services_atlas_search_similar, app_services_atlas_vector_search_pipeline, app_services_gemini_answer [EXTRACTED 1.00]
- **Agent Instructions, Scoped Rules & Skills Surface** — agents_architecture, gemini_customizations, claude_instructions, rule_routers, rule_services, rule_models_tests, skill_add_endpoint, skill_atlas_index [EXTRACTED 1.00]

## Communities (14 total, 2 thin omitted)

### Community 0 - "Agent Instructions & Rules"
Cohesion: 0.08
Nodes (28): health(), Request, Attach X-Request-ID correlation and X-Process-Time-Ms latency headers., Readiness probe reporting active Gemini and Atlas execution modes (no secrets)., readyz(), telemetry_and_correlation_middleware(), answer(), caption_image() (+20 more)

### Community 1 - "FastAPI Multimodal Routers"
Cohesion: 0.14
Nodes (21): AskRequest, Multimodal question request grounded against retrieved Atlas context., Return a pure MongoDB aggregation pipeline using `$vectorSearch`., vector_search_pipeline(), cosine_similarity(), test_ask_request_accepts_image(), test_ask_request_defaults_top_k(), test_ask_request_rejects_missing_question() (+13 more)

### Community 2 - "Evaluation & Benchmark Harness"
Cohesion: 0.22
Nodes (19): integration, live, _client(), Path, Test suite for the Multimodal Gemini Agent. All unit and integration tests run…, Build a FastAPI TestClient., test_ask_includes_sources_when_retrieved(), test_ask_rejects_invalid_base64() (+11 more)

### Community 3 - "Agent Instructions & Rules"
Cohesion: 0.12
Nodes (18): ask(), post, Answer a question grounded in retrieved Atlas context and optional image., ingest(), post, Request, Ingest a visual document via multipart file upload or JSON `IngestRequest`., Delegate to the Gemini embedding service. (+10 more)

### Community 4 - "Evaluation & Benchmark Harness"
Cohesion: 0.12
Nodes (16): EvalCase, main(), Any, Path, Deterministic evaluation & latency benchmark harness for multimodal-gemini-…, Immutable specification of a single multimodal ingest + ask benchmark case., Execute the offline golden evaluation suite and return a structured scorecard., run_evaluation() (+8 more)

### Community 5 - "MongoDB Atlas Vector Search"
Cohesion: 0.17
Nodes (13): _get_mongo_collection(), Any, MongoDB Atlas Vector Search pipeline builder and document store., Return a live PyMongo collection if `MONGODB_URI` is configured for live use., Store a captioned document and its embedding vector in Atlas (or offline store)., Retrieve the top-k matching documents using Atlas `$vectorSearch` or local…, search_similar(), store_document() (+5 more)

### Community 6 - "FastAPI Multimodal Routers"
Cohesion: 0.19
Nodes (11): AskResponse, IngestRequest, IngestResponse, Pydantic request/response schemas (frozen/immutable DTOs)., Response returned after captioning, embedding, and storing a visual asset., Grounded answer with source document references., JSON payload alternative for ingesting a base64-encoded document., Question-answering router: retrieves vector context and invokes Gemini. (+3 more)

### Community 7 - "Agent Instructions & Rules"
Cohesion: 0.25
Nodes (8): AGENTS.md Portable Instructions, CLAUDE.md Repo Instructions, CONTRIBUTING.md Guide, GEMINI.md Antigravity Config, Models & Tests Rules (.claude/rules/models-and-tests.md), Sample Quarterly Revenue Chart (SVG), Skill: add-multimodal-endpoint, Skill: atlas-vector-index

## Knowledge Gaps
- **9 isolated node(s):** `multimodal-gemini-agent`, `Skill: add-multimodal-endpoint`, `GitHub Actions CI Workflow`, `CLAUDE.md Repo Instructions`, `CONTRIBUTING.md Guide` (+4 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 66 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ingest()` connect `Agent Instructions & Rules` to `Agent Instructions & Rules`, `MongoDB Atlas Vector Search`, `FastAPI Multimodal Routers`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Why does `vector_search_pipeline()` connect `FastAPI Multimodal Routers` to `Agent Instructions & Rules`, `Evaluation & Benchmark Harness`, `MongoDB Atlas Vector Search`, `Agent Instructions & Rules`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Why does `run_evaluation()` connect `Evaluation & Benchmark Harness` to `Evaluation & Benchmark Harness`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **What connects `multimodal-gemini-agent`, `Skill: add-multimodal-endpoint`, `GitHub Actions CI Workflow` to the rest of the system?**
  _9 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Agent Instructions & Rules` be split into smaller, more focused modules?**
  _Cohesion score 0.07954545454545454 - nodes in this community are weakly interconnected._
- **Should `FastAPI Multimodal Routers` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._
- **Should `Agent Instructions & Rules` be split into smaller, more focused modules?**
  _Cohesion score 0.12418300653594772 - nodes in this community are weakly interconnected._