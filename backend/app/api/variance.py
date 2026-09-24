from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from schemas.variance import MonthlyVariance
from app.services.variance_service import calculate_variance


router = APIRouter(
    prefix="/api/financial",
    tags=["Financial"],
)


@router.get(
    "/variance",
    response_model=MonthlyVariance,
)
def get_variance(
    previous_month: str = Query(
        ...,
        pattern=r"^\d{4}-\d{2}$",
    ),
    current_month: str = Query(
        ...,
        pattern=r"^\d{4}-\d{2}$",
    ),
    db: Session = Depends(get_db),
):
    return calculate_variance(
        previous_month=previous_month,
        current_month=current_month,
        db=db,
    )