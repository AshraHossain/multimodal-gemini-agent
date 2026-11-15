from fastapi import FastAPI

from app.routers import ask, ingest

app = FastAPI(title="Multimodal Gemini Agent")
app.include_router(ingest.router)
app.include_router(ask.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
