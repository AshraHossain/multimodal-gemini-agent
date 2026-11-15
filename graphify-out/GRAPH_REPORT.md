# Graph Report - multimodal-gemini-agent  (2026-11-15)

## Corpus Check
- Corpus is ~5,618 words - fits in a single context window. You may not need a graph.

## Summary
- 116 nodes · 226 edges · 12 communities (7 shown, 1 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Embedding & Similarity
- Schemas & Validation
- FastAPI Routing & Services
- Atlas Vector Search
- Gemini Multimodal Service
- Test Suite & Coverage
- Module Group 6
- Module Group 11

## God Nodes (most connected - your core abstractions)
1. `ingest()` - 12 edges
2. `_client()` - 12 edges
3. `AskRequest` - 10 edges
4. `vector_search_pipeline()` - 10 edges
5. `test_gemini_validation_and_live_sdk_branch()` - 9 edges
6. `ask()` - 8 edges
7. `search_similar()` - 8 edges
8. `rank_by_similarity()` - 8 edges
9. `IngestResponse` - 7 edges
10. `AskResponse` - 7 edges

## Surprising Connections (you probably didn't know these)
- `test_ingest_response_fields()` --uses--> `IngestResponse`  [INFERRED]
  tests/test_suite.py → app/models/schemas.py
- `test_ask_request_accepts_image()` --uses--> `AskRequest`  [INFERRED]
  tests/test_suite.py → app/models/schemas.py
- `test_ask_request_defaults_top_k()` --uses--> `AskRequest`  [INFERRED]
  tests/test_suite.py → app/models/schemas.py
- `test_ask_request_rejects_missing_question()` --uses--> `AskRequest`  [INFERRED]
  tests/test_suite.py → app/models/schemas.py
- `test_schemas_are_immutable()` --uses--> `AskRequest`  [INFERRED]
  tests/test_suite.py → app/models/schemas.py

## Import Cycles
- None detected.

## Communities (12 total, 1 thin omitted)

### Community 0 - "Embedding & Similarity"
Cohesion: 0.18
Nodes (24): AskRequest, Multimodal question request grounded against retrieved Atlas context., Return a pure MongoDB aggregation pipeline using `$vectorSearch`., vector_search_pipeline(), cosine_similarity(), rank_by_similarity(), Return the top-k candidates (each having an 'embedding') by cosine sim. Each…, Test suite for the Multimodal Gemini Agent. All unit and integration tests run… (+16 more)

### Community 1 - "Schemas & Validation"
Cohesion: 0.13
Nodes (17): IngestRequest, IngestResponse, Pydantic request/response schemas (frozen/immutable DTOs)., Response returned after captioning, embedding, and storing a visual asset., JSON payload alternative for ingesting a base64-encoded document., ingest(), post, Ingestion router: captions, embeds, and stores visual documents (including… (+9 more)

### Community 2 - "FastAPI Routing & Services"
Cohesion: 0.15
Nodes (14): answer(), caption_image(), _deterministic_vector(), embed_text(), _get_live_api_key(), Gemini multimodal reasoning and embedding service. Isolates the Google Gemini…, Generate a grounded answer from retrieved context and optional visual input., Return a live API key if configured, or None when running in offline/mock mode. (+6 more)

### Community 3 - "Atlas Vector Search"
Cohesion: 0.14
Nodes (13): health(), AskResponse, Grounded answer with source document references., ask(), post, Question-answering router: retrieves vector context and invokes Gemini., Answer a question grounded in retrieved Atlas context and optional image., Embedding helpers. ``to_vector`` calls Gemini (needs an API key in live mode)… (+5 more)

### Community 4 - "Gemini Multimodal Service"
Cohesion: 0.23
Nodes (14): integration, live, _client(), Build a FastAPI TestClient., test_ask_includes_sources_when_retrieved(), test_ask_rejects_invalid_base64(), test_ask_returns_answer_field(), test_end_to_end_ingest_then_ask() (+6 more)

### Community 5 - "Test Suite & Coverage"
Cohesion: 0.24
Nodes (9): Any, _get_mongo_collection(), MongoDB Atlas Vector Search pipeline builder and document store., Return a live PyMongo collection if `MONGODB_URI` is configured for live use., Store a captioned document and its embedding vector in Atlas (or offline store)., Retrieve the top-k matching documents using Atlas `$vectorSearch` or local…, search_similar(), store_document() (+1 more)

### Community 6 - "Module Group 6"
Cohesion: 0.29
Nodes (7): Clear the offline in-memory document store (used by test fixtures)., reset_memory_store(), fixture, FixtureRequest, MonkeyPatch, _clean_offline_environment(), Force offline deterministic mode unless running a `@pytest.mark.live` test.

## Knowledge Gaps
- **1 isolated node(s):** `multimodal-gemini-agent`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 47 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ingest()` connect `Schemas & Validation` to `FastAPI Routing & Services`, `Atlas Vector Search`, `Test Suite & Coverage`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Why does `test_gemini_validation_and_live_sdk_branch()` connect `FastAPI Routing & Services` to `Embedding & Similarity`, `Module Group 6`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `_clean_offline_environment()` connect `Module Group 6` to `Embedding & Similarity`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `AskRequest` (e.g. with `ask()` and `test_ask_request_accepts_image()`) actually correct?**
  _`AskRequest` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `multimodal-gemini-agent` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Schemas & Validation` be split into smaller, more focused modules?**
  _Cohesion score 0.13450292397660818 - nodes in this community are weakly interconnected._
- **Should `Atlas Vector Search` be split into smaller, more focused modules?**
  _Cohesion score 0.14166666666666666 - nodes in this community are weakly interconnected._