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


def _normalized_amount(transaction: Transaction) -> Decimal:
    """
    Normalize transaction amounts for financial comparison.

    Revenue:
        Keep the original sign.

    Expenses / COGS:
        Convert negative bank outflows into positive cost values.

    Refunds / discounts:
        Keep the original sign because they reduce revenue.
    """

    amount = Decimal(str(transaction.amount))

    if transaction.category in COGS_CATEGORIES:
        return abs(amount)

    if transaction.category in OPERATING_EXPENSE_CATEGORIES:
        return abs(amount)

    return amount


def calculate_variance(
    previous_month: str,
    current_month: str,
    db: Session,
) -> dict:

    transactions = (
        db.query(Transaction)
        .filter(
            Transaction.accounting_treatment == "P&L"
        )
        .all()
    )

    previous = defaultdict(lambda: Decimal("0"))
    current = defaultdict(lambda: Decimal("0"))

    for transaction in transactions:

        month = transaction.date.strftime("%Y-%m")

        amount = _normalized_amount(transaction)

        if month == previous_month:
            previous[transaction.category] += amount

        elif month == current_month:
            current[transaction.category] += amount

    categories = set(previous) | set(current)

    drivers = []

    for category in categories:

        previous_amount = previous[category]
        current_amount = current[category]

        change = current_amount - previous_amount

        if previous_amount != 0:
            change_percent = (
                change / abs(previous_amount)
            ) * Decimal("100")
        else:
            change_percent = None

        drivers.append(
            {
                "category": category,
                "previous_amount": previous_amount,
                "current_amount": current_amount,
                "change": change,
                "change_percent": change_percent,
            }
        )

    # Calculate operating profit
    previous_operating_profit = _calculate_operating_profit(
        previous
    )

    current_operating_profit = _calculate_operating_profit(
        current
    )

    operating_profit_change = (
        current_operating_profit
        - previous_operating_profit
    )

    if previous_operating_profit != 0:
        operating_profit_change_percent = (
            operating_profit_change
            / abs(previous_operating_profit)
        ) * Decimal("100")
    else:
        operating_profit_change_percent = None

    # Largest absolute category changes first
    drivers.sort(
        key=lambda item: abs(item["change"]),
        reverse=True,
    )

    # Evidence from current month
    top_categories = {
        driver["category"]
        for driver in drivers[:5]
    }

    evidence = [
        transaction
        for transaction in transactions
        if (
            transaction.date.strftime("%Y-%m")
            == current_month
            and transaction.category in top_categories
        )
    ]

    evidence = sorted(
        evidence,
        key=lambda transaction: abs(
            Decimal(str(transaction.amount))
        ),
        reverse=True,
    )

    return {
        "previous_month": previous_month,
        "current_month": current_month,
        "previous_operating_profit": previous_operating_profit,
        "current_operating_profit": current_operating_profit,
        "operating_profit_change": operating_profit_change,
        "operating_profit_change_percent": (
            operating_profit_change_percent
        ),
        "drivers": drivers,
        "evidence": [
            {
                "transaction_id": transaction.transaction_id,
                "date": transaction.date.isoformat(),
                "description": transaction.description,
                "counterparty": transaction.counterparty,
                "amount": transaction.amount,
                "category": transaction.category,
            }
            for transaction in evidence[:20]
        ],
    }


def _calculate_operating_profit(
    category_amounts: dict,
) -> Decimal:

    revenue = category_amounts["Revenue"]

    # Refunds / discounts reduce revenue
    revenue += category_amounts["Refunds & Discounts"]

    cogs = sum(
        category_amounts[category]
        for category in COGS_CATEGORIES
    )

    operating_expenses = sum(
        category_amounts[category]
        for category in OPERATING_EXPENSE_CATEGORIES
    )

    return revenue - cogs - operating_expenses