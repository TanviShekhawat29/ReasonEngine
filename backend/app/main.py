from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.api.v1.upload import router as upload_router
from app.api.v1.extract import router as extract_router
from app.api.v1.chunk import router as chunk_router
from app.api.v1.retrieve import router as retrieve_router
from app.api.v1.ask import router as ask_router
from app.api.v1.document import router as document_router

from app.core.logging import logger
from app.core.resources import resources

from app.services.document_service import DocumentService


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Initializing application resources...")

    # Embeddings
    app.state.embedding_service = resources.embedding_service

    # Vector Database
    app.state.vector_store = resources.vector_store

    # Indexer
    app.state.document_indexer = resources.document_indexer

    # Retriever
    app.state.retriever = resources.retriever

    # LLM
    app.state.llm_service = resources.llm_service

    # Document Intelligence
    app.state.document_intelligence = resources.document_intelligence

    # Services
    # Services
    app.state.document_service = DocumentService(
        indexer=resources.document_indexer,
        intelligence=resources.document_intelligence,
    )

    logger.info("Reason Engine Server Started")

    yield

    logger.info("Closing application resources...")

    app.state.vector_store.client.close()

    logger.info("Reason Engine Server Shutdown")


app = FastAPI(
    title="Reason Engine API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(upload_router, prefix="/api/v1")
app.include_router(extract_router, prefix="/api/v1")
app.include_router(chunk_router, prefix="/api/v1")
app.include_router(retrieve_router, prefix="/api/v1")
app.include_router(document_router, prefix="/api/v1")
app.include_router(ask_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Reason Engine API is running."
    }