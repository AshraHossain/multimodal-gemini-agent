---
paths:
  - "app/models/**/*.py"
  - "tests/**/*.py"
---
# Models & Testing Rules (`app/models/`, `tests/`)

1. **Immutable Schemas (`app/models/schemas.py`)**:
   - Every Pydantic `BaseModel` must declare `model_config = ConfigDict(frozen=True)`.
   - Use `Field(...)` constraints (`min_length=1`, `ge=1`, `le=50`) to enforce input validation at the schema boundary.
2. **Offline Deterministic Tests (`tests/`)**:
   - All tests executed by default (`uv run pytest`) must run offline with `GEMINI_MOCK=1` and `ATLAS_MOCK=1` and reset the in-memory store via fixture.
   - Categorize every test with `@pytest.mark.unit`, `@pytest.mark.integration`, or `@pytest.mark.live`.
   - Maintain >=80% coverage across `app/` (`uv run pytest --cov=app --cov-report=term-missing`).
   - Never commit `@pytest.mark.skip` placeholders without a corresponding tracked item in `TASK.md`.
