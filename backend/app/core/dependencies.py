from fastapi import Request

from app.services.document_service import DocumentService
from app.services.document_intelligence import DocumentIntelligenceService

from app.retrieval.embeddings import EmbeddingService
from app.retrieval.vector_store import VectorStore
from app.retrieval.indexer import DocumentIndexer
from app.retrieval.retriever import Retriever

from app.llm.service import LLMService


def get_embedding_service(request: Request) -> EmbeddingService:
    return request.app.state.embedding_service


def get_vector_store(request: Request) -> VectorStore:
    return request.app.state.vector_store


def get_indexer(request: Request) -> DocumentIndexer:
    return request.app.state.document_indexer


def get_document_service(request: Request) -> DocumentService:
    return request.app.state.document_service


def get_retriever(request: Request) -> Retriever:
    return request.app.state.retriever


def get_llm_service(request: Request) -> LLMService:
    return request.app.state.llm_service


def get_document_intelligence(
    request: Request,
) -> DocumentIntelligenceService:
    return request.app.state.document_intelligence