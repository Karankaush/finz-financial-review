from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from schemas.transaction import (
    TransactionCorrection,
    TransactionResponse,
)
from app.services.transaction_service import (
    correct_transaction,
    get_transactions_needing_review,
)


router = APIRouter(
    prefix="/api/transactions",
    tags=["Transactions"],
)


@router.get(
    "/review",
    response_model=list[TransactionResponse],
)
def get_review_transactions(
    db: Session = Depends(get_db),
):
    return get_transactions_needing_review(db)


@router.put(
    "/{transaction_id}/classification",
    response_model=TransactionResponse,
)
def update_transaction_classification(
    transaction_id: int,
    correction: TransactionCorrection,
    db: Session = Depends(get_db),
):
    try:
        return correct_transaction(
            transaction_id=transaction_id,
            category=correction.category,
            accounting_treatment=correction.accounting_treatment,
            db=db,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )