# Contributing to multimodal-gemini-agent

This is an early-stage FastAPI scaffold. Read [PLANNING.md](PLANNING.md)
first — it documents the current architecture, module responsibilities, and
what's actually implemented vs. stubbed (both `/ingest` and `/ask`, and all
of `app/services/gemini.py`, currently `raise NotImplementedError`) so you
don't rediscover that from scratch.

## Development Setup

Dependency management is [UV](https://docs.astral.sh/uv/)-based
(`pyproject.toml` + `uv.lock`):

```bash
uv sync
uv run pytest
```

`requirements.txt` is also kept in sync for tooling that expects it, but
`uv sync` is the source of truth for the resolved environment.

Run the service locally:

```bash
cp .env.example .env   # set GEMINI_API_KEY + MONGODB_URI
uv run uvicorn app.main:app --reload
```

## Framework

This repo follows the SuperClaude Framework structure — see
[PLANNING.md](PLANNING.md) for architecture and [TASK.md](TASK.md) for the
prioritized backlog. Check `TASK.md` before starting work; the stubbed
routes and Gemini service functions are already tracked there.

## Guidelines

- Keep `app/models/schemas.py` the single source of truth for
  request/response shapes; don't add ad hoc dicts alongside it.
- New Gemini calls go in `app/services/gemini.py`; new Atlas/vector-search
  logic goes in `app/services/atlas.py`. Keep routers in `app/routers/`
  thin — they should orchestrate service calls, not contain SDK logic.
- `app/services/atlas.py`'s `vector_search_pipeline` is pure (no DB
  connection) and unit-tested — keep it that way; put any real MongoDB
  client/connection code in a separate function.
- Unskip the corresponding test in `tests/test_suite.py` when you implement
  a stubbed route or service function (see the `@pytest.mark.skip` reasons).
- Conventional commits: `feat|fix|test|refactor|docs|chore(scope): description`.

## Definition of done

- `uv run pytest` green, with previously-skipped tests unskipped as the
  features they cover are implemented.
- New behavior documented in `PLANNING.md` if it changes the architecture
  or request flow.
