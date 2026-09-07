from pathlib import Path
from uuid import uuid4
import shutil

from fastapi import (
    APIRouter,
    File,
    UploadFile,
    HTTPException,
    Depends,
)

from app.core.logging import logger

from app.services.document_service import DocumentService
from app.services.document_intelligence import DocumentIntelligenceService

from app.core.dependencies import (
    get_document_service,
    get_document_intelligence,
)

router = APIRouter(tags=["Upload"])

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    document_service: DocumentService = Depends(get_document_service),
    intelligence: DocumentIntelligenceService = Depends(
        get_document_intelligence
    ),
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    original_filename = file.filename

    stored_filename = f"{uuid4()}.pdf"

    destination = UPLOAD_FOLDER / stored_filename

    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    logger.info(f"Uploaded PDF: {original_filename}")

    # -----------------------------
    # Index document
    # -----------------------------

    result = document_service.process_document(
        str(destination),
        original_filename,
    )

    # -----------------------------
    # Extract full text
    # -----------------------------

    extracted = document_service.extract_document(
        str(destination)
    )

    # -----------------------------
    # Generate document intelligence
    # -----------------------------

    intelligence.process(
        extracted["text"]
    )

    return {
        "message": "PDF uploaded and indexed successfully.",

        "stored_filename": stored_filename,

        "original_filename": original_filename,

        "pages": result["pages"],

        "characters": result["characters"],

        "chunks": result["chunks"],

        "vectors": result["vectors"],

        "summary_generated": intelligence.get_summary() is not None,

        "questions_generated": (
            intelligence.get_questions() is not None
        ),
    }