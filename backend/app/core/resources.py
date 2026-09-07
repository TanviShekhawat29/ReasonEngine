from app.retrieval.embeddings import EmbeddingService
from app.retrieval.vector_store import VectorStore
from app.retrieval.indexer import DocumentIndexer
from app.retrieval.retriever import Retriever

from app.llm.service import LLMService
from app.services.document_intelligence import DocumentIntelligenceService


class AppResources:
    """
    Stores heavyweight singleton resources.
    """

    def __init__(self):

        # Embedding model
        self.embedding_service = EmbeddingService()

        # Vector database
        self.vector_store = VectorStore()

        # Indexer
        self.document_indexer = DocumentIndexer(
            embedding_service=self.embedding_service,
            vector_store=self.vector_store,
        )

        # Retriever
        self.retriever = Retriever(
            embedding_service=self.embedding_service,
            vector_store=self.vector_store,
        )

        # LLM
        self.llm_service = LLMService()

        # Document Intelligence
        self.document_intelligence = DocumentIntelligenceService(
            llm_service=self.llm_service
        )


resources = AppResources()