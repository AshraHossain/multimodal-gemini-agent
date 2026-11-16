# Security Policy & Threat Model

## Threat Model & Mitigations

| Threat Vector | Risk | Mitigation Implemented |
|---|---|---|
| **Indirect Prompt Injection via Visual Assets** | Malicious instructions embedded inside uploaded charts/PDFs attempting to hijack `POST /ask` generation. | `gemini.sanitize_untrusted_text()` neutralizes boundary-escape tags and wraps retrieved captions inside `<untrusted_context>` XML data boundaries with explicit system instructions to treat contents as passive data. |
| **Unauthorized API Access** | Unauthenticated callers invoking `/ingest` or `/ask` in shared environments. | Timing-safe API key verification (`hmac.compare_digest`) via `X-API-Key` or `Authorization: Bearer <token>` when `API_AUTH_TOKEN` is set (`HTTP 401 Unauthorized`), while keeping `/health` and `/readyz` unauthenticated for container probes. |
| **Abuse / Denial of Wallet (`429`)** | Burst traffic exhausting LLM quotas or vector search compute. | Sliding-window rate limiter (`RATE_LIMIT_PER_MINUTE`, default `120` req/min) returning `HTTP 429 Too Many Requests` with `Retry-After: 60`. |
| **Unbounded Payload / DoS (`413`)** | Oversized uploads or base64 blobs exhausting memory. | Enforced `MAX_UPLOAD_BYTES = 10 MB` on both `POST /ingest` and `POST /ask` (`HTTP 413 Payload Too Large`) and `max_length=4000` on `AskRequest.question`. |
| **Path Traversal & Document ID Injection** | Malicious filenames (`../../etc/passwd`) or special characters in `source_id`. | `ingest.sanitize_doc_id()` strips directory components (`os.path.basename`), replaces unsafe characters, and caps length at 128 chars. |
| **Arbitrary File Type Ingestion (`415`)** | Executables or unsupported binary blobs uploaded to `/ingest`. | Strict `ALLOWED_MIME_TYPES` allowlist (`image/png`, `image/jpeg`, `image/webp`, `image/svg+xml`, `application/pdf`), returning `HTTP 415 Unsupported Media Type`. |
| **OWASP HTTP Response Hardening** | MIME sniffing, clickjacking, or caching of sensitive responses. | Middleware sets `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, `Cache-Control: no-store`, and `Content-Security-Policy: default-src 'none'; frame-ancestors 'none'`. |
| **Static Security Scanning (`S` / Bandit)** | Insecure Python constructs introduced in PRs. | Ruff flake8-bandit (`S`) rules enabled in `pyproject.toml` and enforced on every push in `.github/workflows/ci.yml`. |
| **Container Privilege Escalation** | Running the FastAPI server as `root` inside Docker. | Multi-stage `Dockerfile` runs as unprivileged `appuser` (`UID 10001`). |

## Reporting a Vulnerability

Please report security issues privately via GitHub Security Advisories rather than opening a public issue.
