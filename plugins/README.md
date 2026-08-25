# plugins/

Reserved for SuperClaude Framework plugin extensions for this project (e.g.
alternative embedding providers, a swappable vector-store backend, or eval
harnesses packaged as plugins).

No plugins are defined yet. `multimodal-gemini-agent` currently calls Gemini
and MongoDB Atlas directly from `app/services/` (`gemini.py`, `atlas.py`,
`embedding.py`) rather than through an installable plugin interface — see
`PLANNING.md` for the current (mostly stubbed) service layer.
