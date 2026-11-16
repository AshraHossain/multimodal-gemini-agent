from __future__ import annotations

import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response

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


@app.middleware("http")
async def telemetry_and_correlation_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Attach X-Request-ID correlation and X-Process-Time-Ms latency headers."""
    req_id = request.headers.get("X-Request-ID") or f"req-{uuid.uuid4().hex[:12]}"
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000.0
    response.headers["X-Request-ID"] = req_id
    response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"
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
