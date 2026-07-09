"""MongoDB Atlas Vector Search. TODO: implement."""
def vector_search_pipeline(vector: list[float], k: int = 4, index: str = "vector_index") -> list[dict]:
    """Return an aggregation pipeline using $vectorSearch."""
    return [{"$vectorSearch": {"index": index, "path": "embedding",
            "queryVector": vector, "numCandidates": k * 10, "limit": k}}]
