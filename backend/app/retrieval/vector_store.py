from typing import List
import hashlib

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)


class VectorStore:
    """
    Handles all interactions with the Qdrant vector database.
    """

    COLLECTION_NAME = "reason_engine"

    def __init__(self):
        self.client = QdrantClient(path="./qdrant_data")
        self._create_collection()

    def _create_collection(self):
        collections = self.client.get_collections().collections
        names = [collection.name for collection in collections]

        if self.COLLECTION_NAME not in names:
            self.client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE,
                ),
            )

    def clear_collection(self):
        """
        Clears all vectors before indexing a new document.
        This project supports one active document at a time.
        """

        try:
            self.client.delete_collection(self.COLLECTION_NAME)
        except Exception:
            pass

        self.client.create_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

    def add_documents(
        self,
        chunks: List[str],
        embeddings: List[List[float]],
        filename: str,
    ):
        """
        Stores document chunks.
        """

        points = []

        for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):

            point_id = hashlib.md5(
                f"{filename}:{index}".encode("utf-8")
            ).hexdigest()

            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "text": chunk,
                        "source": filename,
                        "chunk_index": index,
                    },
                )
            )

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=points,
        )

    def search(
        self,
        embedding: List[float],
        limit: int = 3,
    ):
        results = self.client.search(
            collection_name=self.COLLECTION_NAME,
            query_vector=embedding,
            limit=limit,
        )

        return [
            {
                "text": hit.payload["text"],
                "source": hit.payload["source"],
                "score": round(hit.score, 4),
            }
            for hit in results
        ]

    def count(self):
        result = self.client.count(
            collection_name=self.COLLECTION_NAME,
            exact=True,
        )

        return result.count