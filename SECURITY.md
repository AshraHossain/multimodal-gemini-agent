# Security Policy & Threat Model

## Threat Model & Mitigations

| Threat Vector | Risk | Mitigation Implemented |
|---|---|---|
| **Indirect Prompt Injection via Visual Assets** | Malicious instructions embedded inside uploaded charts/PDFs attempting to hijack `POST /ask` generation. | `gemini.sanitize_untrusted_text()` neutralizes boundary-escape tags and wraps retrieved captions inside `<untrusted_context>` XML data boundaries with explicit system instructions to treat contents as passive data. |
| **Unbounded Payload / DoS (`POST /ingest`)** | Oversized uploads exhausting memory or downstream token budgets. | Enforced `MAX_UPLOAD_BYTES = 10 MB` at the router boundary (`HTTP 413 Payload Too Large`). |
| **Arbitrary File Type Ingestion** | Executables or unsupported binary blobs uploaded to `/ingest`. | Strict `ALLOWED_MIME_TYPES` allowlist (`image/png`, `image/jpeg`, `image/webp`, `image/svg+xml`, `application/pdf`), returning `HTTP 415 Unsupported Media Type`. |
| **Credential & Stack Trace Leakage** | Upstream SDK exceptions or `.env` keys exposed in HTTP responses. | Secrets (`GEMINI_API_KEY`, `MONGODB_URI`) are read exclusively from environment variables in `app/services/`; `/readyz` reports only mode names (`live` vs `offline-mock`). |
| **Container Privilege Escalation** | Running the FastAPI server as `root` inside Docker. | Multi-stage `Dockerfile` runs as unprivileged `appuser` (`UID 10001`). |

## Reporting a Vulnerability

Please report security issues privately via GitHub Security Advisories rather than opening a public issue.
