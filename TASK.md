# TASK.md — multimodal-gemini-agent

Priority task list. See `PLANNING.md` for architecture context.

## High priority

- [ ] **Implement `app/services/gemini.py`** — `caption_image`,
  `embed_text`, and `answer` all currently `raise NotImplementedError`.
  Everything downstream (`/ingest`, `/ask`, `embedding.to_vector`) depends
  on this.
- [ ] **Implement `POST /ingest`** (`app/routers/ingest.py`) — currently
  `raise NotImplementedError`. Should caption the uploaded image/PDF page,
  embed it, and store it in MongoDB Atlas, returning an `IngestResponse`.
- [ ] **Implement `POST /ask`** (`app/routers/ask.py`) — currently
  `raise NotImplementedError`. Should embed the question, run
  `atlas.vector_search_pipeline` against Atlas, and call `gemini.answer`
  with the retrieved context (+ optional image) to build an `AskResponse`.
- [ ] **Wire an actual MongoDB client into `app/services/atlas.py`** — today
  it only builds the `$vectorSearch` aggregation-pipeline list
  (`vector_search_pipeline`); there is no connection or `.aggregate()` call
  yet.

## Medium priority

- [ ] **Unskip tests as implementation lands** — 7 of the 24 tests in
  `tests/test_suite.py` are `@pytest.mark.skip`'d pending the above
  (the file's own docstring says "20-test suite," which is stale — verified
  24 collected via `uv run pytest --collect-only`)
  (`test_ingest_returns_doc_id`, `test_ask_returns_answer_field`,
  `test_ask_includes_sources_when_retrieved`, `test_caption_image_returns_text`,
  `test_embed_text_returns_vector_of_expected_dim`,
  `test_answer_uses_image_when_provided`, and the integration test
  `test_end_to_end_ingest_then_ask`).
- [ ] **Add sample assets under `data/`** — the README quickstart references
  sample charts/diagrams in `data/`, which doesn't exist in the repo yet.
- [ ] **Document/verify the Atlas index creation** — README references a
  vector index named `vector_index` on the `embedding` field; add a
  startup check or setup script once `atlas.py` has real connection code.

## Low priority / infra

- [x] Git repository initialized, MIT license in place (correct copyright
  holder — not changed by this migration).
- [x] UV-based dependency management added (`pyproject.toml` + `uv.lock`),
  alongside the existing `requirements.txt`.
- [ ] Dockerfile for containerized runs — not present yet.
- [ ] CI workflow (lint/test on push) — not yet configured.
