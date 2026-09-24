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
    review_only: bool = False,
) -> list[Transaction]:

    query = db.query(Transaction)

    if review_only:
        query = query.filter(
            Transaction.needs_review.is_(True)
        )

    return (
        query
        .order_by(Transaction.date.desc())
        .limit(limit)
        .all()
    )


def _is_review_question(question: str) -> bool:
    keywords = [
        "review",
        "attention",
        "uncertain",
        "unclassified",
        "needs attention",
    ]

    question_lower = question.lower()

    return any(
        keyword in question_lower
        for keyword in keywords
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

    transactions = _build_transaction_context(
    db,
    review_only=_is_review_question(question),
)

    pnl_context = _serialize_pnl(pnl_data)

    transaction_context = _serialize_transactions(
        transactions
    )

    prompt = f"""
You are an AI financial analyst for a restaurant business.

The backend has already performed the financial calculations
and transaction filtering.

Your job is to explain the provided data clearly.
You are NOT responsible for deciding which transactions
belong in the provided dataset.

IMPORTANT RULES:

1. Never invent financial numbers.
2. Never invent transaction IDs.
3. Never include transactions that are not relevant to
   the user's question.
4. If the transaction context contains transactions marked
   as needing review, treat that as the authoritative list
   of transactions requiring review.
5. Do not add transactions merely because they seem
   financially interesting.
6. Do not include transactions that are explicitly marked
   as not requiring review when answering a review question.
7. Do not perform unsupported accounting reclassification.
8. If the provided data is insufficient, say so.
9. Keep the answer concise and easy to scan.
10. Use Markdown headings, bullets, or tables only when
    they improve readability.
11. Mention transaction IDs when they are relevant evidence.
12. If there are many transactions, summarize the total
    count and show only the 10 most relevant transactions.
13. Do not list every transaction unless the user explicitly
    asks for the complete list.
14. Prefer a short summary followed by a small table or
    bullet list when appropriate.

MONTHLY P&L:

{pnl_context}

TRANSACTION DATA:

{transaction_context}

USER QUESTION:

{question}

Answer format:

- Start with a direct one-sentence answer.
- Then provide the key details using short bullets
  or a small Markdown table.
- If there are many transactions, show only the
  10 most relevant ones.
- Do not include unrelated transactions.
- End with a short "Evidence" section containing
  the relevant transaction IDs.
"""

    llm = ChatGroq(
        model=settings.GROQ_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=0,
    )

    response = llm.invoke(prompt)

    evidence = [
    transaction.transaction_id
    for transaction in transactions
    ]
    return {
        "answer": response.content,
        "evidence": evidence,
    }