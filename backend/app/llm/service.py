from app.llm.client import client
from app.core.config import settings
from app.llm.prompts import (
    SYSTEM_PROMPT,
    DOCUMENT_SUMMARY_PROMPT,
    DOCUMENT_QUESTIONS_PROMPT,
)


class LLMService:
    """
    Handles all interactions with Groq.
    """

    def _chat(self, system_prompt: str, user_prompt: str) -> str:
        completion = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return completion.choices[0].message.content.strip()

    def generate_answer(
        self,
        question: str,
        context: str,
    ):
        return self._chat(
            SYSTEM_PROMPT.format(context=context),
            question,
        )

    def generate_document_summary(
        self,
        context: str,
    ):
        return self._chat(
            DOCUMENT_SUMMARY_PROMPT.format(context=context),
            "Summarize this document.",
        )

    def generate_document_questions(
        self,
        context: str,
    ):
        response = self._chat(
            DOCUMENT_QUESTIONS_PROMPT.format(context=context),
            "Generate questions.",
        )

        return [
            q.strip("-•1234567890. ")
            for q in response.split("\n")
            if q.strip()
        ]

    def calculate_confidence(
        self,
        retrieved_chunks: list,
    ):
        if not retrieved_chunks:
            return {
                "confidence": 0,
                "reason": "No relevant document chunks found."
            }

        avg_score = sum(
            chunk["score"] for chunk in retrieved_chunks
        ) / len(retrieved_chunks)

        confidence = min(100, int(avg_score * 100))

        if confidence >= 85:
            reason = "High similarity retrieved from document."
        elif confidence >= 70:
            reason = "Good similarity retrieved."
        elif confidence >= 50:
            reason = "Moderate similarity retrieved."
        else:
            reason = "Low similarity. Answer may be incomplete."

        return {
            "confidence": confidence,
            "reason": reason,
        }