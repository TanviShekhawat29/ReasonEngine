from pathlib import Path

from fastapi import APIRouter, HTTPException, Depends

from app.core.logging import logger
from app.services.document_service import DocumentService
from app.core.dependencies import get_document_service

router = APIRouter(tags=["Extraction"])

UPLOAD_FOLDER = Path("uploads")


@router.get("/extract/{filename}")
async def extract_pdf(
    filename: str,
    document_service: DocumentService = Depends(get_document_service),
):

    pdf_path = UPLOAD_FOLDER / filename

    if not pdf_path.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF not found.",
        )

    logger.info(f"Extracting {filename}")

    result = document_service.extract_document(str(pdf_path))

    return {
        "filename": filename,
        "pages": result["pages"],
        "characters": result["characters"],
        "text": result["text"],
    }