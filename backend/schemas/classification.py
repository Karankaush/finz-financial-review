from pydantic import BaseModel


class ClassificationResponse(BaseModel):
    message: str
    classified_transactions: int
    transactions_needing_review: int