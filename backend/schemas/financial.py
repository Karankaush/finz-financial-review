from decimal import Decimal

from pydantic import BaseModel


class MonthlyPnL(BaseModel):
    month: str

    revenue: Decimal
    cogs: Decimal
    gross_profit: Decimal

    operating_expenses: Decimal
    operating_profit: Decimal