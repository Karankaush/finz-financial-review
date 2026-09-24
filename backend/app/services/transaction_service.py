from sqlalchemy.orm import Session

from app.models.transaction import Transaction


def get_transactions_needing_review(
    db: Session,
) -> list[Transaction]:

    return (
        db.query(Transaction)
        .filter(Transaction.needs_review.is_(True))
        .order_by(Transaction.date.asc())
        .all()
    )


def correct_transaction(
    transaction_id: int,
    category: str,
    accounting_treatment: str,
    db: Session,
) -> Transaction:

    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )

    if transaction is None:
        raise ValueError("Transaction not found")

    transaction.category = category
    transaction.accounting_treatment = accounting_treatment
    transaction.user_correction = category
    transaction.confidence = 1.0
    transaction.needs_review = False

    db.commit()
    db.refresh(transaction)

    return transaction