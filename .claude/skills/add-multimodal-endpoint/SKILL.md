---
name: add-multimodal-endpoint
description: >-
  Use this skill when adding or modifying a FastAPI endpoint, Pydantic schema,
  or Gemini/Atlas service function in multimodal-gemini-agent. Guides strict TDD,
  frozen schema definition, pure service isolation, and offline test verification.
---

# Add or Update a Multimodal Endpoint

Follow this repo-specific procedure whenever adding or modifying a route or service capability in `multimodal-gemini-agent`.

## Steps

1. **Define Frozen Schemas (`app/models/schemas.py`)**
   - Add or update request/response models with `model_config = ConfigDict(frozen=True)` and explicit `Field` constraints (`min_length`, `ge`, `le`).

2. **Write Failing Offline Tests First (`tests/test_suite.py`)**
   - Add `@pytest.mark.unit` tests for schema validation and service functions (both offline deterministic mode and injected mock client/collection).
   - Add `@pytest.mark.integration` tests using FastAPI `TestClient` covering happy path and `400`/`422` validation errors.
   - Run `uv run pytest` and confirm the new tests fail for the expected reason (RED).

3. **Implement Service Logic (`app/services/`)**
   - Keep pure calculations/pipelines (`atlas.vector_search_pipeline`, `embedding.rank_by_similarity`) free of I/O.
   - Ensure any new function in `app/services/gemini.py` or `app/services/atlas.py` supports `GEMINI_MOCK=1` / `ATLAS_MOCK=1` offline execution as well as live `google.genai` / `pymongo` execution.

4. **Wire Thin Router (`app/routers/` & `app/main.py`)**
   - Decode and validate inputs at the HTTP boundary, call `app/services/`, and return the frozen Pydantic response model.

5. **Verify Coverage, Lint, and Docs**
   - Run `uv run ruff check .`
   - Run `uv run pytest --cov=app --cov-report=term-missing` and verify coverage remains >=80%.
   - Update `PLANNING.md` and `TASK.md` if architecture or backlog status changed.
