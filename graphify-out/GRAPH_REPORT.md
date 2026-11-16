# Graph Report - multimodal-gemini-agent  (2026-11-15)

## Corpus Check
- Corpus is ~7,400 words - fits in a single context window. You may not need a graph.

## Summary
- 148 nodes · 280 edges · 16 communities (8 shown, 4 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Module Group 0
- Module Group 1
- Module Group 2
- Module Group 3
- Module Group 4
- Module Group 5
- Module Group 6
- Module Group 7
- Module Group 12
- Module Group 13
- Module Group 14
- Module Group 15

## God Nodes (most connected - your core abstractions)
1. `ingest()` - 14 edges
2. `_client()` - 14 edges
3. `vector_search_pipeline()` - 12 edges
4. `AskRequest` - 11 edges
5. `ask()` - 9 edges
6. `test_gemini_validation_and_live_sdk_branch()` - 9 edges
7. `run_evaluation()` - 8 edges
8. `search_similar()` - 8 edges
9. `rank_by_similarity()` - 8 edges
10. `caption_image()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Router Layer Rules (.claude/rules/routers.md)` --rationale_for--> `ingest()`  [EXTRACTED]
  /Users/ashraf-macbookair/projects/multimodal-gemini-agent/.claude/rules/routers.md → app/routers/ingest.py
- `SECURITY.md Threat Model` --rationale_for--> `ingest()`  [EXTRACTED]
  /Users/ashraf-macbookair/projects/multimodal-gemini-agent/SECURITY.md → app/routers/ingest.py
- `Service Layer Rules (.claude/rules/services.md)` --rationale_for--> `vector_search_pipeline()`  [EXTRACTED]
  /Users/ashraf-macbookair/projects/multimodal-gemini-agent/.claude/rules/services.md → app/services/atlas.py
- `Models & Tests Rules (.claude/rules/models-and-tests.md)` --rationale_for--> `AskRequest`  [EXTRACTED]
  /Users/ashraf-macbookair/projects/multimodal-gemini-agent/.claude/rules/models-and-tests.md → app/models/schemas.py
- `Router Layer Rules (.claude/rules/routers.md)` --rationale_for--> `ask()`  [EXTRACTED]
  /Users/ashraf-macbookair/projects/multimodal-gemini-agent/.claude/rules/routers.md → app/routers/ask.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Ask Pipeline: Embed -> Search Similar -> Multimodal Answer** — app_routers_ask_ask, app_services_embedding_to_vector, app_services_atlas_search_similar, app_services_atlas_vector_search_pipeline, app_services_gemini_answer [EXTRACTED 1.00]

## Communities (16 total, 4 thin omitted)

### Community 0 - "Module Group 0"
Cohesion: 0.13
Nodes (23): AskRequest, Multimodal question request grounded against retrieved Atlas context., Return a pure MongoDB aggregation pipeline using `$vectorSearch`., vector_search_pipeline(), cosine_similarity(), Models & Tests Rules (.claude/rules/models-and-tests.md), Sample Quarterly Revenue Chart (SVG), Skill: atlas-vector-index (+15 more)

### Community 1 - "Module Group 1"
Cohesion: 0.12
Nodes (19): answer(), caption_image(), _deterministic_vector(), embed_text(), _get_live_api_key(), Gemini multimodal reasoning and embedding service. Isolates the Google Gemini…, Embed text into a float vector of length `dim`., Generate a grounded answer from retrieved context and optional visual input. (+11 more)

### Community 2 - "Module Group 2"
Cohesion: 0.22
Nodes (19): integration, live, _client(), Path, Test suite for the Multimodal Gemini Agent. All unit and integration tests run…, Build a FastAPI TestClient., test_ask_includes_sources_when_retrieved(), test_ask_rejects_invalid_base64() (+11 more)

### Community 3 - "Module Group 3"
Cohesion: 0.13
Nodes (17): IngestRequest, IngestResponse, Pydantic request/response schemas (frozen/immutable DTOs)., Response returned after captioning, embedding, and storing a visual asset., JSON payload alternative for ingesting a base64-encoded document., ingest(), post, Request (+9 more)

### Community 4 - "Module Group 4"
Cohesion: 0.13
Nodes (15): EvalCase, main(), Any, Path, Deterministic evaluation & latency benchmark harness for multimodal-gemini-…, Immutable specification of a single multimodal ingest + ask benchmark case., Execute the offline golden evaluation suite and return a structured scorecard., run_evaluation() (+7 more)

### Community 5 - "Module Group 5"
Cohesion: 0.17
Nodes (13): _get_mongo_collection(), Any, MongoDB Atlas Vector Search pipeline builder and document store., Return a live PyMongo collection if `MONGODB_URI` is configured for live use., Store a captioned document and its embedding vector in Atlas (or offline store)., Retrieve the top-k matching documents using Atlas `$vectorSearch` or local…, search_similar(), store_document() (+5 more)

### Community 6 - "Module Group 6"
Cohesion: 0.18
Nodes (11): AskResponse, Grounded answer with source document references., ask(), post, Question-answering router: retrieves vector context and invokes Gemini., Answer a question grounded in retrieved Atlas context and optional image., Embedding helpers. ``to_vector`` calls Gemini (needs an API key in live mode)…, Delegate to the Gemini embedding service. (+3 more)

### Community 7 - "Module Group 7"
Cohesion: 0.22
Nodes (9): health(), Request, Attach X-Request-ID correlation and X-Process-Time-Ms latency headers., Readiness probe reporting active Gemini and Atlas execution modes (no secrets)., readyz(), telemetry_and_correlation_middleware(), get, middleware (+1 more)

## Knowledge Gaps
- **6 isolated node(s):** `multimodal-gemini-agent`, `Models & Tests Rules (.claude/rules/models-and-tests.md)`, `Skill: add-multimodal-endpoint`, `CONTRIBUTING.md Guide`, `GEMINI.md Antigravity Config` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 63 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ingest()` connect `Module Group 3` to `Module Group 1`, `Module Group 5`, `Module Group 6`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Why does `vector_search_pipeline()` connect `Module Group 0` to `Module Group 1`, `Module Group 2`, `Module Group 5`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `test_gemini_validation_and_live_sdk_branch()` connect `Module Group 1` to `Module Group 0`, `Module Group 2`, `Module Group 4`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **What connects `multimodal-gemini-agent`, `Models & Tests Rules (.claude/rules/models-and-tests.md)`, `Skill: add-multimodal-endpoint` to the rest of the system?**
  _6 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Module Group 0` be split into smaller, more focused modules?**
  _Cohesion score 0.12648221343873517 - nodes in this community are weakly interconnected._
- **Should `Module Group 1` be split into smaller, more focused modules?**
  _Cohesion score 0.11857707509881422 - nodes in this community are weakly interconnected._
- **Should `Module Group 3` be split into smaller, more focused modules?**
  _Cohesion score 0.13450292397660818 - nodes in this community are weakly interconnected._