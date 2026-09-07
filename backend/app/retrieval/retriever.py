from app.retrieval.embeddings import EmbeddingService
from app.retrieval.vector_store import VectorStore


class Retriever:
    """
    Retrieves the most relevant chunks for a query.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ):
        embedding = self.embedding_service.embed_text(query)

        return self.vector_store.search(
            embedding=embedding,
            limit=limit,
        )