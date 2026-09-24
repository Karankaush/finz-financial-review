from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from schemas.classification import ClassificationResponse
from app.services.classification_service import classify_transactions


router = APIRouter(
    prefix="/api/classification",
    tags=["Classification"],
)


@router.post(
    "/run",
    response_model=ClassificationResponse,
)
def run_classification(
    db: Session = Depends(get_db),
):
    try:
        total, review_count = classify_transactions(db)

        return ClassificationResponse(
            message="Transactions classified successfully",
            classified_transactions=total,
            transactions_needing_review=review_count,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )