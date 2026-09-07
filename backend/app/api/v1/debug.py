from fastapi import APIRouter, Depends

from app.core.dependencies import get_vector_store
from app.retrieval.vector_store import VectorStore

router = APIRouter(tags=["Debug"])


@router.get("/debug/vector-store")
def debug_vector_store(
    vector_store: VectorStore = Depends(get_vector_store),
):
    count = vector_store.count()

    results = vector_store.search(
        embedding=[0.0] * 384,
        limit=10,
    )

    return {
        "count": count,
        "sources": [r["source"] for r in results],
    }