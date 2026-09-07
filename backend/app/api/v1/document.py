from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_document_service
from app.services.document_service import DocumentService

from app.api.v1.models.document import (
    DocumentSummaryResponse,
    SuggestedQuestionsResponse,
)

router = APIRouter(tags=["Document Intelligence"])


@router.get(
    "/document/summary",
    response_model=DocumentSummaryResponse,
)
async def document_summary(
    document_service: DocumentService = Depends(get_document_service),
):

    result = document_service.get_document_summary()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="No document uploaded.",
        )

    return result


@router.get(
    "/document/questions",
    response_model=SuggestedQuestionsResponse,
)
async def suggested_questions(
    document_service: DocumentService = Depends(get_document_service),
):

    result = document_service.get_suggested_questions()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="No document uploaded.",
        )

    return result