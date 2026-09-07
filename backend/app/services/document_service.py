from app.ingestion.pdf_reader import extract_text_from_pdf
from app.retrieval.chunker import split_text
from app.services.document_intelligence import DocumentIntelligenceService


class DocumentService:

    def __init__(
        self,
        indexer,
        intelligence: DocumentIntelligenceService,
    ):
        self.indexer = indexer
        self.intelligence = intelligence

    def extract_document(
        self,
        pdf_path: str,
    ):
        return extract_text_from_pdf(pdf_path)

    def chunk_document(
        self,
        pdf_path: str,
    ):
        result = extract_text_from_pdf(pdf_path)

        chunks = split_text(result["text"])

        return {
            "pages": result["pages"],
            "characters": result["characters"],
            "text": result["text"],
            "chunks": chunks,
            "total_chunks": len(chunks),
        }

    def process_document(
        self,
        pdf_path: str,
        filename: str,
    ):

        extracted = extract_text_from_pdf(pdf_path)

        indexed = self.indexer.index_document(
            extracted["text"],
            filename,
        )

        self.intelligence.process(
            extracted["text"]
        )

        return {
            "pages": extracted["pages"],
            "characters": extracted["characters"],
            "chunks": indexed["chunks"],
            "vectors": indexed["vectors"],
        }

    def get_document_summary(self):
        return self.intelligence.get_summary()

    def get_suggested_questions(self):
        return self.intelligence.get_questions()