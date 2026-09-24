from decimal import Decimal

from langchain_groq import ChatGroq
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.transaction import Transaction
from app.services.pnl_service import calculate_monthly_pnl
from app.services.variance_service import calculate_variance


def _serialize_pnl(pnl_data: list[dict]) -> str:
    lines = []

    for month in pnl_data:
        lines.append(
            f"""
Month: {month['month']}
Revenue: {month['revenue']}
COGS: {month['cogs']}
Gross Profit: {month['gross_profit']}
Operating Expenses: {month['operating_expenses']}
Operating Profit: {month['operating_profit']}
"""
        )

    return "\n".join(lines)


def _build_transaction_context(
    db: Session,
    limit: int = 100,
) -> list[Transaction]:

    return (
        db.query(Transaction)
        .order_by(Transaction.date.desc())
        .limit(limit)
        .all()
    )


def _serialize_transactions(
    transactions: list[Transaction],
) -> str:

    lines = []

    for transaction in transactions:
        lines.append(
            f"""
Transaction ID: {transaction.transaction_id}
Date: {transaction.date}
Description: {transaction.description}
Counterparty: {transaction.counterparty}
Amount: {transaction.amount}
Category: {transaction.category}
Accounting Treatment: {transaction.accounting_treatment}
"""
        )

    return "\n".join(lines)


def answer_question(
    question: str,
    db: Session,
) -> dict:

    pnl_data = calculate_monthly_pnl(db)

    transactions = _build_transaction_context(db)

    pnl_context = _serialize_pnl(pnl_data)

    transaction_context = _serialize_transactions(
        transactions
    )

    prompt = f"""
You are an AI financial analyst for a restaurant business.

Answer the user's question using ONLY the financial
data provided below.

IMPORTANT RULES:

1. Never invent financial numbers.
2. Never calculate numbers that are not supported by the
   provided data.
3. Treat the P&L figures below as authoritative.
4. If the data does not contain enough information,
   clearly say so.
5. Explain the reasoning in simple business language.
6. Mention the relevant transaction IDs when discussing
   transaction-level evidence.
7. Do not claim that a transaction caused something unless
   the provided data supports that connection.

MONTHLY P&L:

{pnl_context}

TRANSACTION DATA:

{transaction_context}

USER QUESTION:

{question}

Provide:
1. A concise answer.
2. The relevant transaction IDs or financial periods
   used as evidence.
"""

    llm = ChatGroq(
        model=settings.GROQ_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=0,
    )

    response = llm.invoke(prompt)

    evidence = []

    for transaction in transactions:
        if transaction.transaction_id in response.content:
            evidence.append(transaction.transaction_id)

    return {
        "answer": response.content,
        "evidence": evidence,
    }