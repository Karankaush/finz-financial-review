from collections import defaultdict
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.transaction import Transaction


REVENUE_CATEGORIES = {
    "Revenue",
}

COGS_CATEGORIES = {
    "Food",
    "Beverage",
}

OPERATING_EXPENSE_CATEGORIES = {
    "Payroll",
    "Rent",
    "Utilities",
    "Marketing",
    "Insurance",
    "Cleaning",
    "Delivery Commission",
    "Office/Admin Supplies",
    "Repairs & Maintenance",
    "POS/Software Subscription",
    "Accounting/Bookkeeping",
    "To-go Packaging & Disposables",
}

CONTRA_REVENUE_CATEGORIES = {
    "Refunds & Discounts",
}


def calculate_monthly_pnl(
    db: Session,
) -> list[dict]:

    transactions = (
        db.query(Transaction)
        .filter(Transaction.accounting_treatment == "P&L")
        .order_by(Transaction.date.asc())
        .all()
    )

    monthly = defaultdict(
        lambda: {
            "revenue": Decimal("0"),
            "cogs": Decimal("0"),
            "operating_expenses": Decimal("0"),
        }
    )

    for transaction in transactions:

        month = transaction.date.strftime("%Y-%m")
        amount = Decimal(str(transaction.amount))

        # -------------------------
        # REVENUE
        # -------------------------
        if transaction.category in REVENUE_CATEGORIES:
            monthly[month]["revenue"] += amount

        # -------------------------
        # REFUNDS / DISCOUNTS
        # Contra-revenue
        # -------------------------
        elif transaction.category in CONTRA_REVENUE_CATEGORIES:
            monthly[month]["revenue"] += amount

        # -------------------------
        # COGS
        # -------------------------
        elif transaction.category in COGS_CATEGORIES:
            monthly[month]["cogs"] += abs(amount)

        # -------------------------
        # OPERATING EXPENSES
        # -------------------------
        elif transaction.category in OPERATING_EXPENSE_CATEGORIES:
            monthly[month]["operating_expenses"] += abs(amount)

    results = []

    for month in sorted(monthly):

        revenue = monthly[month]["revenue"]
        cogs = monthly[month]["cogs"]
        operating_expenses = monthly[month]["operating_expenses"]

        # Gross Profit = Revenue - COGS
        gross_profit = revenue - cogs

        # Operating Profit = Gross Profit - Operating Expenses
        operating_profit = (
            gross_profit - operating_expenses
        )

        results.append(
            {
                "month": month,
                "revenue": revenue,
                "cogs": cogs,
                "gross_profit": gross_profit,
                "operating_expenses": operating_expenses,
                "operating_profit": operating_profit,
            }
        )

    return results