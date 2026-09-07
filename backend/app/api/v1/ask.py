from fastapi import APIRouter, Depends

from app.api.v1.models.ask import (
    AskRequest,
    AskResponse,
)

from app.core.dependencies import (
    get_retriever,
    get_llm_service,
)

from app.retrieval.retriever import Retriever
from app.llm.service import LLMService


router = APIRouter(tags=["Question Answering"])


@router.post(
    "/ask",
    response_model=AskResponse,
)
async def ask(
    request: AskRequest,
    retriever: Retriever = Depends(get_retriever),
    llm: LLMService = Depends(get_llm_service),
):

    retrieved_chunks = retriever.retrieve(
        query=request.question,
        limit=request.limit,
    )

    context = ""

    for i, chunk in enumerate(retrieved_chunks, start=1):

        context += f"""
Document Chunk {i}

Source:
{chunk['source']}

Content:
{chunk['text']}

--------------------------------
"""

    answer = llm.generate_answer(
        question=request.question,
        context=context,
    )

    confidence = llm.calculate_confidence(
        retrieved_chunks
    )

    return AskResponse(
        question=request.question,
        answer=answer,
        confidence=confidence["confidence"],
        reason=confidence["reason"],
        sources=retrieved_chunks,
    )