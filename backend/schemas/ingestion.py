from pydantic import BaseModel


class IngestionResponse(BaseModel):
    message: str
    total_transactions: int