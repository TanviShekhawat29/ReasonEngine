from fastapi import APIRouter, Depends

from app.schemas.retrieve import RetrieveRequest
from app.core.dependencies import get_retriever
from app.retrieval.retriever import Retriever

router = APIRouter(tags=["Retrieval"])


@router.post("/retrieve")
async def retrieve(
    request: RetrieveRequest,
    retriever: Retriever = Depends(get_retriever),
):
    results = retriever.retrieve(
        query=request.query,
        limit=request.limit,
    )

    return {
        "query": request.query,
        "results": results,
    }