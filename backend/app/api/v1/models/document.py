from typing import List
from pydantic import BaseModel


class DocumentSummaryResponse(BaseModel):
    title: str
    summary: str
    topics: List[str]


class SuggestedQuestionsResponse(BaseModel):
    questions: List[str]