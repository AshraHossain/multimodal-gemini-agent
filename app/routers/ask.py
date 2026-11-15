"""Question-answering router: retrieves vector context and invokes Gemini."""
from __future__ import annotations

import base64
import binascii

from fastapi import APIRouter, HTTPException

from app.models.schemas import AskRequest, AskResponse
from app.services import atlas, embedding, gemini

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest) -> AskResponse:
    """Answer a question grounded in retrieved Atlas context and optional image."""
    image_bytes: bytes | None = None
    if req.image_b64 is not None:
        try:
            image_bytes = base64.b64decode(req.image_b64, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise HTTPException(status_code=400, detail="Invalid base64 in image_b64") from exc

    query_vector = embedding.to_vector(req.question)
    matches = atlas.search_similar(query_vector, k=req.top_k)

    context_chunks = [str(m.get("text", "")) for m in matches if m.get("text")]
    sources = [
        str(m.get("doc_id", m.get("id", "")))
        for m in matches
        if m.get("doc_id") or m.get("id")
    ]

    grounded_answer = gemini.answer(
        question=req.question,
        context=context_chunks,
        image_bytes=image_bytes,
    )
    return AskResponse(answer=grounded_answer, sources=sources)
