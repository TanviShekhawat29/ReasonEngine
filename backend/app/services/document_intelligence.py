from app.llm.service import LLMService


class DocumentIntelligenceService:
    """
    Generates document-level intelligence once after upload.
    """

    def __init__(self, llm_service: LLMService):

        self.llm = llm_service

        self.title = ""
        self.summary = ""
        self.questions = []
        self.topics = []

    def process(self, text: str):

        context = text[:12000]

        # Generate summary
        self.summary = self.llm.generate_document_summary(context)

        # Generate suggested questions
        self.questions = self.llm.generate_document_questions(context)

        # Default title
        self.title = "Uploaded Document"

        # Build simple topics from questions
        topics = []

        for q in self.questions:
            q = q.replace("?", "").strip()

            words = q.split()

            if len(words) >= 3:
                topics.append(" ".join(words[:3]))

        # Remove duplicates while preserving order
        self.topics = list(dict.fromkeys(topics))[:8]

    def get_summary(self):

        if not self.summary:
            return None

        return {
            "title": self.title,
            "summary": self.summary,
            "topics": self.topics,
        }

    def get_questions(self):

        if not self.questions:
            return None

        return {
            "questions": self.questions
        }