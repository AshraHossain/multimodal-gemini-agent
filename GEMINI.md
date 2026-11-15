# GEMINI.md — Multimodal AI Agent with Gemini

Read and follow [AGENTS.md](AGENTS.md) in this directory for project architecture, verified commands, and repo-specific invariants.

## Antigravity / Gemini Customizations

- **Workspace Skills (`.agents/skills/*/SKILL.md`)**:
  - `add-multimodal-endpoint` — TDD workflow for adding or extending multimodal FastAPI endpoints, frozen Pydantic schemas, and offline-testable Gemini/Atlas service functions.
  - `atlas-vector-index` — Runbook for configuring and verifying the MongoDB Atlas `$vectorSearch` index (`vector_index`).
- **Workspace Rules (`.agents/rules/*.md`)**:
  - `routers.md` — Thin router and boundary validation rules for `app/routers/**/*.py`.
  - `services.md` — SDK isolation, pure pipeline/math separation, and offline mock policy rules for `app/services/**/*.py`.
  - `models-and-tests.md` — Frozen Pydantic schema and offline pytest coverage rules for `app/models/**/*.py` and `tests/**/*.py`.
- **Global Suite**: Inherits global engineering rules, subagents (`planner`, `architect`, `tdd-guide`, `python-reviewer`, `security-reviewer`), and curated skills from the `gemini-core-workflow` plugin (`~/.gemini/config/plugins/gemini-core-workflow/`).
