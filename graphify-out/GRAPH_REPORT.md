# Graph Report - .  (2026-06-19)

## Corpus Check
- Corpus is ~1,267 words - fits in a single context window. You may not need a graph.

## Summary
- 86 nodes · 115 edges · 12 communities (10 shown, 2 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 16 edges (avg confidence: 0.71)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Embedding Similarity|Embedding Similarity]]
- [[_COMMUNITY_API Models & Setup|API Models & Setup]]
- [[_COMMUNITY_Architecture & Routing|Architecture & Routing]]
- [[_COMMUNITY_Vector Search Integration|Vector Search Integration]]
- [[_COMMUNITY_Embedding Service|Embedding Service]]
- [[_COMMUNITY_Gemini AI Integration|Gemini AI Integration]]
- [[_COMMUNITY_Core Embedding Functions|Core Embedding Functions]]
- [[_COMMUNITY_Health Check|Health Check]]

## God Nodes (most connected - your core abstractions)
1. `AskRequest` - 8 edges
2. `vector_search_pipeline()` - 8 edges
3. `AskResponse` - 6 edges
4. `cosine_similarity()` - 6 edges
5. `rank_by_similarity()` - 6 edges
6. `Test Suite` - 6 edges
7. `Atlas Vector Search Service` - 5 edges
8. `Service Layer Architecture Pattern` - 5 edges
9. `POST /ask Endpoint` - 5 edges
10. `IngestResponse` - 4 edges

## Surprising Connections (you probably didn't know these)
- `Atlas Vector Search Service` --implements--> `MongoDB Atlas Vector Search`  [EXTRACTED]
  app/services/atlas.py → README.md
- `Service Layer Architecture Pattern` --implements--> `Atlas Vector Search Service`  [INFERRED]
  CLAUDE.md → app/services/atlas.py
- `Service Layer Architecture Pattern` --implements--> `Embedding Service`  [INFERRED]
  CLAUDE.md → app/services/embedding.py
- `Service Layer Architecture Pattern` --implements--> `Gemini Multimodal Service`  [INFERRED]
  CLAUDE.md → app/services/gemini.py
- `Gemini Multimodal Reasoning Pattern` --implements--> `caption_image Function`  [INFERRED]
  README.md → app/services/gemini.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Ingest Pipeline: Caption → Embed → Store** — func_caption_image, func_to_vector, service_atlas [INFERRED 0.75]
- **Ask Pipeline: Retrieve → Reason → Answer** — service_atlas, service_gemini, endpoint_ask_post [INFERRED 0.75]

## Communities (12 total, 2 thin omitted)

### Community 0 - "Embedding Similarity"
Cohesion: 0.13
Nodes (13): cosine_similarity(), rank_by_similarity(), Return the top-k candidates (each having an 'embedding') by cosine sim.      Eac, _client(), 20-test suite for the Multimodal Gemini Agent.  Tests that exercise pure scaffol, Build a FastAPI TestClient, skipping if FastAPI isn't installed., test_cosine_identical_vectors_is_one(), test_cosine_length_mismatch_raises() (+5 more)

### Community 1 - "API Models & Setup"
Cohesion: 0.14
Nodes (12): AskRequest, BaseModel, AskRequest, AskResponse, IngestResponse, Pydantic request/response schemas., ask(), test_ask_request_accepts_image() (+4 more)

### Community 2 - "Architecture & Routing"
Cohesion: 0.19
Nodes (17): CLAUDE.md Architecture Documentation, POST /ask Endpoint, POST /ingest Endpoint, FastAPI Application, cosine_similarity Function, rank_by_similarity Function, Service Layer Architecture Pattern, Service Isolation Rationale (+9 more)

### Community 3 - "Vector Search Integration"
Cohesion: 0.22
Nodes (8): MongoDB Atlas Vector Search. TODO: implement., Return an aggregation pipeline using $vectorSearch., vector_search_pipeline(), test_pipeline_has_vector_search_stage(), test_pipeline_limit_matches_k(), test_pipeline_num_candidates_scales_with_k(), test_pipeline_path_is_embedding(), test_pipeline_uses_custom_index_name()

### Community 4 - "Embedding Service"
Cohesion: 0.25
Nodes (5): Embedding helpers.  ``to_vector`` calls Gemini (needs an API key) and is impleme, Delegate to the Gemini embedding service (requires GEMINI_API_KEY)., to_vector(), embed_text(), Gemini multimodal + embedding wrapper. TODO: implement.

### Community 5 - "Gemini AI Integration"
Cohesion: 0.40
Nodes (5): README Project Overview, answer Function, caption_image Function, Gemini Multimodal Reasoning Pattern, MongoDB Atlas Vector Search

## Knowledge Gaps
- **8 isolated node(s):** `Ingest Router`, `to_vector Embedding Function`, `caption_image Function`, `embed_text Function`, `answer Function` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `rank_by_similarity()` connect `Embedding Similarity` to `Embedding Service`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Why does `AskRequest` connect `API Models & Setup` to `Embedding Similarity`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `cosine_similarity()` connect `Embedding Similarity` to `Embedding Service`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **What connects `Pydantic request/response schemas.`, `MongoDB Atlas Vector Search. TODO: implement.`, `Return an aggregation pipeline using $vectorSearch.` to the rest of the system?**
  _17 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Embedding Similarity` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Should `API Models & Setup` be split into smaller, more focused modules?**
  _Cohesion score 0.1437908496732026 - nodes in this community are weakly interconnected._