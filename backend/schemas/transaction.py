from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class TransactionResponse(BaseModel):
    id: int
    transaction_id: str
    date: date
    description: str
    counterparty: str
    amount: Decimal
    method: str
    category: str | None
    confidence: Decimal | None
    needs_review: bool
    accounting_treatment: str | None
    user_correction: str | None

    model_config = ConfigDict(from_attributes=True)


class TransactionCorrection(BaseModel):
    category: str
    accounting_treatment: str