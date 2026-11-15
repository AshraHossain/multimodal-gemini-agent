---
paths:
  - "app/services/**/*.py"
---
# Service Layer Rules (`app/services/`)

1. **Pure Core vs. External I/O**:
   - `atlas.vector_search_pipeline(vector, k, index)` must remain 100% pure: return a plain MongoDB `$vectorSearch` stage list without opening a DB connection.
   - `embedding.cosine_similarity` and `embedding.rank_by_similarity` must remain pure math functions and return new dicts (`{**c, "score": score}`) without mutating input candidate dicts.
   - Never delegate vector math, cosine ranking, or threshold calculations to LLM prompts.
2. **Offline-First Determinism**:
   - `gemini.py` and `atlas.py` must respect `GEMINI_MOCK=1` and `ATLAS_MOCK=1` (or missing placeholder credentials) so tests run deterministically offline without live network calls.
   - Accept optional injected `collection` in `atlas.store_document` and `atlas.search_similar` to enable isolated unit testing.
3. **Unified Gemini SDK**:
   - Use `from google import genai` (`google-genai` SDK) for live multimodal generation and embeddings.
   - Validate non-empty `image_bytes`, `text`, and `question` before invoking any SDK or mock path, raising `ValueError` on empty inputs.
