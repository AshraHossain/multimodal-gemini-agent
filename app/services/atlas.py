"""MongoDB Atlas Vector Search pipeline builder and document store."""
from __future__ import annotations

import os
import uuid
from typing import Any

from app.services.embedding import rank_by_similarity

VECTOR_INDEX_DEFINITION: dict[str, Any] = {
    "name": "vector_index",
    "type": "vectorSearch",
    "definition": {
        "fields": [
            {
                "type": "vector",
                "path": "embedding",
                "numDimensions": 768,
                "similarity": "cosine",
            }
        ]
    },
}

# In-memory fallback store used when MONGODB_URI is not configured or in offline tests.
_MEMORY_STORE: tuple[dict[str, Any], ...] = ()


def reset_memory_store() -> None:
    """Clear the offline in-memory document store (used by test fixtures)."""
    global _MEMORY_STORE
    _MEMORY_STORE = ()


def vector_search_pipeline(
    vector: list[float],
    k: int = 4,
    index: str = "vector_index",
) -> list[dict[str, Any]]:
    """Return a pure MongoDB aggregation pipeline using `$vectorSearch`."""
    return [
        {
            "$vectorSearch": {
                "index": index,
                "path": "embedding",
                "queryVector": list(vector),
                "numCandidates": k * 10,
                "limit": k,
            }
        }
    ]


def _get_mongo_collection() -> Any | None:
    """Return a live PyMongo collection if `MONGODB_URI` is configured for live use."""
    if os.environ.get("ATLAS_MOCK", "").lower() in {"1", "true", "yes"}:
        return None
    uri = os.environ.get("MONGODB_URI", "").strip()
    if not uri or "user:pass@cluster.mongodb.net" in uri:
        return None
    from pymongo import MongoClient

    client: MongoClient[dict[str, Any]] = MongoClient(uri, serverSelectionTimeoutMS=3000)
    db_name = os.environ.get("MONGODB_DB", "multimodal")
    coll_name = os.environ.get("MONGODB_COLLECTION", "documents")
    return client[db_name][coll_name]


def store_document(
    text: str,
    embedding: list[float],
    doc_id: str | None = None,
    metadata: dict[str, Any] | None = None,
    collection: Any | None = None,
) -> dict[str, Any]:
    """Store a captioned document and its embedding vector in Atlas (or offline store)."""
    global _MEMORY_STORE
    resolved_id = doc_id or f"doc-{uuid.uuid4().hex[:8]}"
    record: dict[str, Any] = {
        "doc_id": resolved_id,
        "text": text,
        "embedding": list(embedding),
        "metadata": dict(metadata) if metadata else {},
    }
    target_collection = collection if collection is not None else _get_mongo_collection()
    if target_collection is not None:
        target_collection.insert_one({**record})
    else:
        _MEMORY_STORE = (*_MEMORY_STORE, record)
    return record


def search_similar(
    query_vector: list[float],
    k: int = 4,
    index: str | None = None,
    collection: Any | None = None,
) -> list[dict[str, Any]]:
    """Retrieve the top-k matching documents using Atlas `$vectorSearch` or local fallback."""
    resolved_index = index or os.environ.get("VECTOR_INDEX", "vector_index")
    target_collection = collection if collection is not None else _get_mongo_collection()
    if target_collection is not None:
        pipeline = vector_search_pipeline(query_vector, k=k, index=resolved_index)
        return list(target_collection.aggregate(pipeline))

    if not _MEMORY_STORE:
        return []
    return rank_by_similarity(query_vector, list(_MEMORY_STORE), k=k)
