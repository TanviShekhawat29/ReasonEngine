from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(default=3, ge=1, le=10)


class Source(BaseModel):
    source: str
    score: float
    text: str


class AskResponse(BaseModel):
    query: str
    answer: str
    sources: list[Source]