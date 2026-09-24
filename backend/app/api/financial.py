from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from schemas.financial import MonthlyPnL
from app.services.pnl_service import calculate_monthly_pnl


router = APIRouter(
    prefix="/api/financial",
    tags=["Financial"],
)


@router.get(
    "/pnl",
    response_model=list[MonthlyPnL],
)
def get_monthly_pnl(
    db: Session = Depends(get_db),
):
    return calculate_monthly_pnl(db)