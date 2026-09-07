from typing import List

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Generates vector embeddings using Sentence Transformers.
    """

    def __init__(self):
        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for one text.
        """
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return embedding.tolist()

    def embed_documents(
        self,
        documents: List[str]
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple documents.
        """

        embeddings = self.model.encode(
            documents,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return embeddings.tolist()