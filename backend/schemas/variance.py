from decimal import Decimal

from pydantic import BaseModel


class CategoryVariance(BaseModel):
    category: str
    previous_amount: Decimal
    current_amount: Decimal
    change: Decimal
    change_percent: Decimal | None


class TransactionEvidence(BaseModel):
    transaction_id: str
    date: str
    description: str
    counterparty: str
    amount: Decimal
    category: str


class MonthlyVariance(BaseModel):
    previous_month: str
    current_month: str

    previous_operating_profit: Decimal
    current_operating_profit: Decimal

    operating_profit_change: Decimal
    operating_profit_change_percent: Decimal | None

    drivers: list[CategoryVariance]
    evidence: list[TransactionEvidence]