'''from app.retrieval.chunker import split_text


class DocumentIndexer:
    """
    Splits documents into chunks, generates embeddings,
    and stores them in the vector database.
    """

    def __init__(
        self,
        embedding_service,
        vector_store,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def index_document(
        self,
        text: str,
        filename: str,
    ):
        chunks = split_text(text)

        embeddings = self.embedding_service.embed_documents(chunks)

        # Keep only the latest uploaded document
        self.vector_store.clear_collection()

        self.vector_store.add_documents(
            chunks=chunks,
            embeddings=embeddings,
            filename=filename,
        )

        return {
            "chunks": len(chunks),
            "vectors": self.vector_store.count(),
        }'''

from app.retrieval.chunker import split_text


class DocumentIndexer:
    """
    Splits documents into chunks, generates embeddings,
    and stores them in the vector database.
    """

    def __init__(
        self,
        embedding_service,
        vector_store,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def index_document(
        self,
        text: str,
        filename: str,
    ):

        print("=" * 60)
        print("INDEXING:", filename)
        print("TEXT LENGTH:", len(text))

        chunks = split_text(text)

        print("CHUNKS:", len(chunks))

        embeddings = self.embedding_service.embed_documents(chunks)

        print("EMBEDDINGS:", len(embeddings))

        self.vector_store.clear_collection()

        before = self.vector_store.count()
        print("BEFORE UPSERT:", before)

        self.vector_store.add_documents(
            chunks=chunks,
            embeddings=embeddings,
            filename=filename,
        )

        after = self.vector_store.count()
        print("AFTER UPSERT:", after)
        print("=" * 60)

        return {
            "chunks": len(chunks),
            "vectors": after,
        }