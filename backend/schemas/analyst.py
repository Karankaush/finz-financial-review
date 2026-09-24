from pydantic import BaseModel


class AnalystRequest(BaseModel):
    question: str


class AnalystResponse(BaseModel):
    answer: str
    evidence: list[str]