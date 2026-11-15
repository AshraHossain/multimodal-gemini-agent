# Contributing to multimodal-gemini-agent

Read [AGENTS.md](AGENTS.md) and [PLANNING.md](PLANNING.md) first for the current architecture, module boundaries, and request flow.

## Development Setup

Dependency management is [UV](https://docs.astral.sh/uv/)-based (`pyproject.toml` + `uv.lock`):

```bash
uv sync
uv run ruff check .
uv run pytest --cov=app --cov-report=term-missing
```

Run the service locally:

```bash
cp .env.example .env   # set GEMINI_API_KEY + MONGODB_URI (or leave defaults for offline mock mode)
uv run uvicorn app.main:app --reload
```

## Guidelines

- Keep `app/models/schemas.py` the single source of truth for request/response shapes (`ConfigDict(frozen=True)`).
- Keep `app/routers/` thin — validate HTTP/base64 inputs and delegate SDK/DB work to `app/services/`.
- Keep `app/services/atlas.py`'s `vector_search_pipeline` and `app/services/embedding.py`'s `cosine_similarity` / `rank_by_similarity` pure and side-effect-free.
- Follow the path-scoped rules in `.agents/rules/` (`.claude/rules/`) and repo skills in `.agents/skills/` (`.claude/skills/`).
- Conventional commits: `feat|fix|test|refactor|docs|chore(scope): description`.

## Definition of Done

- `uv run ruff check .` clean.
- `uv run pytest --cov=app --cov-fail-under=80` green (all default tests running offline).
- Architecture changes reflected in `PLANNING.md` and `TASK.md`.
