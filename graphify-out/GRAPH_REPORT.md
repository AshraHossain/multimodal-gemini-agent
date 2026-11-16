# Graph Report - multimodal-gemini-agent  (2026-11-15)

## Corpus Check
- Corpus is ~5,618 words - fits in a single context window. You may not need a graph.

## Summary
- 130 nodes · 245 edges · 14 communities (8 shown, 2 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FastAPI Multimodal Routers
- MongoDB Atlas Vector Search
- Agent Instructions & Rules
- Agent Instructions & Rules
- FastAPI Multimodal Routers
- MongoDB Atlas Vector Search
- Agent Instructions & Rules
- MongoDB Atlas Vector Search
- Test Suite & Verification (12)
- Agent Instructions & Rules

## God Nodes (most connected - your core abstractions)
1. `ingest()` - 14 edges
2. `vector_search_pipeline()` - 12 edges
3. `_client()` - 12 edges
4. `AskRequest` - 11 edges
5. `ask()` - 10 edges
6. `test_gemini_validation_and_live_sdk_branch()` - 9 edges
7. `search_similar()` - 8 edges
8. `rank_by_similarity()` - 8 edges
9. `AGENTS.md Portable Instructions` - 8 edges
10. `IngestResponse` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Models & Tests Rules (.claude/rules/models-and-tests.md)` --rationale_for--> `AskRequest`  [EXTRACTED]
  .claude/rules/models-and-tests.md → app/models/schemas.py
- `Skill: atlas-vector-index` --references--> `vector_search_pipeline()`  [EXTRACTED]
  .claude/skills/atlas-vector-index/SKILL.md → app/services/atlas.py
- `Service Layer Rules (.claude/rules/services.md)` --rationale_for--> `vector_search_pipeline()`  [EXTRACTED]
  .claude/rules/services.md → app/services/atlas.py
- `test_ask_request_defaults_top_k()` --uses--> `AskRequest`  [INFERRED]
  tests/test_suite.py → app/models/schemas.py
- `test_ask_request_rejects_missing_question()` --uses--> `AskRequest`  [INFERRED]
  tests/test_suite.py → app/models/schemas.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Ingest Pipeline: Split -> Caption -> Embed -> Store** — app_routers_ingest_ingest, app_services_gemini_split_visual_chunks, app_services_gemini_caption_image, app_services_embedding_to_vector, app_services_atlas_store_document [EXTRACTED 1.00]
- **Ask Pipeline: Embed -> Search Similar -> Multimodal Answer** — app_routers_ask_ask, app_services_embedding_to_vector, app_services_atlas_search_similar, app_services_atlas_vector_search_pipeline, app_services_gemini_answer [EXTRACTED 1.00]
- **Agent Instructions, Scoped Rules & Skills Surface** — agents_architecture, gemini_customizations, claude_instructions, rule_routers, rule_services, rule_models_tests, claude_skills_add_multimodal_endpoint_skill_add_endpoint, claude_skills_atlas_vector_index_skill_atlas_index [EXTRACTED 1.00]

## Communities (14 total, 2 thin omitted)

### Community 0 - "FastAPI Multimodal Routers"
Cohesion: 0.12
Nodes (18): health(), AskRequest, AskResponse, IngestRequest, IngestResponse, Pydantic request/response schemas (frozen/immutable DTOs)., Response returned after captioning, embedding, and storing a visual asset., Multimodal question request grounded against retrieved Atlas context. (+10 more)

### Community 1 - "MongoDB Atlas Vector Search"
Cohesion: 0.15
Nodes (20): Return a pure MongoDB aggregation pipeline using `$vectorSearch`., vector_search_pipeline(), cosine_similarity(), rank_by_similarity(), Return the top-k candidates (each having an 'embedding') by cosine sim. Each…, test_ask_request_defaults_top_k(), test_ask_request_rejects_missing_question(), test_cosine_identical_vectors_is_one() (+12 more)

### Community 2 - "Agent Instructions & Rules"
Cohesion: 0.12
Nodes (19): ask(), post, Answer a question grounded in retrieved Atlas context and optional image., ingest(), post, Ingest a visual document via multipart file upload or JSON `IngestRequest`., Delegate to the Gemini embedding service., to_vector() (+11 more)

### Community 3 - "Agent Instructions & Rules"
Cohesion: 0.14
Nodes (15): answer(), caption_image(), _deterministic_vector(), embed_text(), _get_live_api_key(), Gemini multimodal reasoning and embedding service. Isolates the Google Gemini…, Generate a grounded answer from retrieved context and optional visual input., Return a live API key if configured, or None when running in offline/mock mode. (+7 more)

### Community 4 - "FastAPI Multimodal Routers"
Cohesion: 0.28
Nodes (15): integration, live, _client(), Test suite for the Multimodal Gemini Agent. All unit and integration tests run…, Build a FastAPI TestClient., test_ask_includes_sources_when_retrieved(), test_ask_rejects_invalid_base64(), test_ask_returns_answer_field() (+7 more)

### Community 5 - "MongoDB Atlas Vector Search"
Cohesion: 0.24
Nodes (9): Any, _get_mongo_collection(), MongoDB Atlas Vector Search pipeline builder and document store., Return a live PyMongo collection if `MONGODB_URI` is configured for live use., Store a captioned document and its embedding vector in Atlas (or offline store)., Retrieve the top-k matching documents using Atlas `$vectorSearch` or local…, search_similar(), store_document() (+1 more)

### Community 6 - "Agent Instructions & Rules"
Cohesion: 0.25
Nodes (8): AGENTS.md Portable Instructions, CLAUDE.md Repo Instructions, Skill: add-multimodal-endpoint, Skill: atlas-vector-index, CONTRIBUTING.md Guide, Sample Quarterly Revenue Chart (SVG), GEMINI.md Antigravity Config, Models & Tests Rules (.claude/rules/models-and-tests.md)

### Community 7 - "MongoDB Atlas Vector Search"
Cohesion: 0.29
Nodes (7): Clear the offline in-memory document store (used by test fixtures)., reset_memory_store(), fixture, FixtureRequest, MonkeyPatch, _clean_offline_environment(), Force offline deterministic mode unless running a `@pytest.mark.live` test.

## Knowledge Gaps
- **9 isolated node(s):** `multimodal-gemini-agent`, `GEMINI.md Antigravity Config`, `CLAUDE.md Repo Instructions`, `TASK.md Completed Milestones`, `README.md Project Overview` (+4 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 55 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ingest()` connect `Agent Instructions & Rules` to `FastAPI Multimodal Routers`, `Agent Instructions & Rules`, `MongoDB Atlas Vector Search`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Why does `vector_search_pipeline()` connect `MongoDB Atlas Vector Search` to `Agent Instructions & Rules`, `FastAPI Multimodal Routers`, `MongoDB Atlas Vector Search`, `Agent Instructions & Rules`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Why does `ask()` connect `Agent Instructions & Rules` to `FastAPI Multimodal Routers`, `Agent Instructions & Rules`, `MongoDB Atlas Vector Search`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `AskRequest` (e.g. with `ask()` and `test_ask_request_accepts_image()`) actually correct?**
  _`AskRequest` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `multimodal-gemini-agent`, `GEMINI.md Antigravity Config`, `CLAUDE.md Repo Instructions` to the rest of the system?**
  _9 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FastAPI Multimodal Routers` be split into smaller, more focused modules?**
  _Cohesion score 0.1225296442687747 - nodes in this community are weakly interconnected._
- **Should `MongoDB Atlas Vector Search` be split into smaller, more focused modules?**
  _Cohesion score 0.14736842105263157 - nodes in this community are weakly interconnected._