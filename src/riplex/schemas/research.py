from pydantic import BaseModel, Field, HttpUrl

class RequestResearch(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=500,
    )

class Source(BaseModel):
    title: str = Field(min_length=1)
    url: HttpUrl
    snippet: str = Field(max_length=2000, min_length=1)
    publication_date: str | None = None

class ResearchReport(BaseModel):
    question: str
    answer: str
    sources: list[Source]