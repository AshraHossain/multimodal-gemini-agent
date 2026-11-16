# plugins/

Extension directory for custom ingestion adapters, alternative embedding providers, or evaluation plugins.

Core multimodal reasoning and vector search are implemented directly in `app/services/gemini.py` (`google-genai`) and `app/services/atlas.py` (`pymongo` `$vectorSearch`), while agent-level customizations live in `.agents/` (`.claude/`) and the global `gemini-core-workflow` Antigravity plugin.
