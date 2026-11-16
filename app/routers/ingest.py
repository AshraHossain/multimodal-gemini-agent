"""Ingestion router: captions, embeds, and stores visual documents (including multi-page PDFs)."""
from __future__ import annotations

import base64
import binascii
import os
import re
import uuid
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Request, UploadFile

from app.models.schemas import IngestRequest, IngestResponse
from app.services import atlas, embedding, gemini

router = APIRouter()

ALLOWED_MIME_TYPES: frozenset[str] = frozenset(
    {
        "image/png",
        "image/jpeg",
        "image/webp",
        "image/svg+xml",
        "application/pdf",
    }
)
MAX_UPLOAD_BYTES: int = 10 * 1024 * 1024  # 10 MB
_SAFE_DOC_ID_RE = re.compile(r"[^A-Za-z0-9._-]+")


def sanitize_doc_id(raw_id: str | None) -> str:
    """Sanitize caller-supplied filenames/IDs to prevent path traversal or NoSQL key injection."""
    if not raw_id:
        return f"doc-{uuid.uuid4().hex[:8]}"
    base = os.path.basename(raw_id.replace("\\", "/")).strip()
    cleaned = _SAFE_DOC_ID_RE.sub("_", base).strip("._-")
    if not cleaned:
        return f"doc-{uuid.uuid4().hex[:8]}"
    return cleaned[:128]


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
        mime_type = (file.content_type or "image/png").split(";")[0].strip().lower()
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
            mime_type = req.mime_type.split(";")[0].strip().lower()
            doc_id = req.source_id
        else:
            raw = await request.body()
            if raw:
                image_bytes = raw

    if not image_bytes:
        raise HTTPException(status_code=400, detail="No visual document bytes provided")

    if mime_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported media type '{mime_type}'. Allowed: {sorted(ALLOWED_MIME_TYPES)}",
        )

    if len(image_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Payload size {len(image_bytes)} bytes exceeds {MAX_UPLOAD_BYTES} byte limit",
        )

    base_doc_id = sanitize_doc_id(doc_id)
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
