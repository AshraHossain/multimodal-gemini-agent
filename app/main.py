from __future__ import annotations

import hmac
import os
import time
import uuid
from collections import deque
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from app.routers import ask, ingest
from app.services import atlas, gemini

app = FastAPI(
    title="Multimodal Gemini Agent",
    version="0.2.0",
    description=(
        "Enterprise multimodal document Q&A with Google Gemini and MongoDB Atlas Vector Search."
    ),
)
app.include_router(ingest.router)
app.include_router(ask.router)

_PROTECTED_PATHS: frozenset[str] = frozenset({"/ingest", "/ask"})
_REQUEST_TIMESTAMPS: deque[float] = deque()

SECURITY_HEADERS: dict[str, str] = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Cache-Control": "no-store",
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
}


def reset_rate_limiter() -> None:
    """Reset the in-memory sliding-window rate limiter (used by test fixtures)."""
    _REQUEST_TIMESTAMPS.clear()


def _check_api_auth(request: Request) -> bool:
    """Verify timing-safe API token when `API_AUTH_TOKEN` is configured."""
    expected_token = os.environ.get("API_AUTH_TOKEN", "").strip()
    if not expected_token:
        return True
    provided = request.headers.get("X-API-Key", "").strip()
    if not provided:
        auth_header = request.headers.get("Authorization", "").strip()
        if auth_header.lower().startswith("bearer "):
            provided = auth_header[7:].strip()
    if not provided:
        return False
    return hmac.compare_digest(provided.encode("utf-8"), expected_token.encode("utf-8"))


def _check_rate_limit(now: float) -> bool:
    """Enforce sliding-window rate limit (`RATE_LIMIT_PER_MINUTE`, default 120)."""
    limit = int(os.environ.get("RATE_LIMIT_PER_MINUTE", "120"))
    window_start = now - 60.0
    while _REQUEST_TIMESTAMPS and _REQUEST_TIMESTAMPS[0] < window_start:
        _REQUEST_TIMESTAMPS.popleft()
    if len(_REQUEST_TIMESTAMPS) >= limit:
        return False
    _REQUEST_TIMESTAMPS.append(now)
    return True


@app.middleware("http")
async def security_and_telemetry_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Enforce auth, rate limiting, OWASP security headers, X-Request-ID, and latency telemetry."""
    req_id = request.headers.get("X-Request-ID") or f"req-{uuid.uuid4().hex[:12]}"
    start = time.perf_counter()

    if request.url.path in _PROTECTED_PATHS:
        if not _check_api_auth(request):
            response: Response = JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized: missing or invalid API token"},
            )
        elif not _check_rate_limit(start):
            response = JSONResponse(
                status_code=429,
                content={"detail": "Too Many Requests: rate limit exceeded"},
                headers={"Retry-After": "60"},
            )
        else:
            response = await call_next(request)
    else:
        response = await call_next(request)

    elapsed_ms = (time.perf_counter() - start) * 1000.0
    response.headers["X-Request-ID"] = req_id
    response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"
    for header_name, header_val in SECURITY_HEADERS.items():
        response.headers.setdefault(header_name, header_val)
    return response


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict[str, str]:
    """Readiness probe reporting active Gemini and Atlas execution modes (no secrets)."""
    gemini_mode = "live" if gemini._get_live_api_key() is not None else "offline-mock"
    atlas_mode = "live" if atlas._get_mongo_collection() is not None else "in-memory-fallback"
    return {
        "status": "ready",
        "version": app.version,
        "gemini_mode": gemini_mode,
        "atlas_mode": atlas_mode,
    }
