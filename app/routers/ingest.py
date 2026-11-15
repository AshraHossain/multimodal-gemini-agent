"""Ingestion router: captions, embeds, and stores visual documents (including multi-page PDFs)."""
from __future__ import annotations

import base64
import binascii
import uuid
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Request, UploadFile

from app.models.schemas import IngestRequest, IngestResponse
from app.services import atlas, embedding, gemini

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
async def ingest(
    request: Request,
    file: Annotated[UploadFile | None, File()] = None,
) -> IngestResponse:
    """Ingest a visual document via multipart file upload or JSON `IngestRequest`."""
    image_bytes: bytes | None = None
    mime_type = "image/png"
    doc_id: str | None = None

    if file is not None:
        image_bytes = await file.read()
        mime_type = file.content_type or "image/png"
        doc_id = file.filename
    else:
        content_type = request.headers.get("content-type", "")
        if "application/json" in content_type:
            body = await request.json()
            req = IngestRequest.model_validate(body)
            try:
                image_bytes = base64.b64decode(req.image_b64, validate=True)
            except (binascii.Error, ValueError) as exc:
                raise HTTPException(
                    status_code=400, detail="Invalid base64 image payload"
                ) from exc
            mime_type = req.mime_type
            doc_id = req.source_id
        else:
            raw = await request.body()
            if raw:
                image_bytes = raw

    if not image_bytes:
        raise HTTPException(status_code=400, detail="No visual document bytes provided")

    base_doc_id = doc_id or f"doc-{uuid.uuid4().hex[:8]}"
    page_chunks = gemini.split_visual_chunks(image_bytes, mime_type=mime_type)

    for idx, chunk_bytes in enumerate(page_chunks, start=1):
        chunk_id = base_doc_id if len(page_chunks) == 1 else f"{base_doc_id}#page-{idx}"
        caption = gemini.caption_image(chunk_bytes, mime_type=mime_type)
        vector = embedding.to_vector(caption)
        atlas.store_document(
            text=caption,
            embedding=vector,
            doc_id=chunk_id,
            metadata={
                "parent_doc_id": base_doc_id,
                "page": idx,
                "total_pages": len(page_chunks),
                "mime_type": mime_type,
                "size_bytes": len(chunk_bytes),
            },
        )

    return IngestResponse(doc_id=base_doc_id, chunks=len(page_chunks))
