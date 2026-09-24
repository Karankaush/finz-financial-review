from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from schemas.analyst import (
    AnalystRequest,
    AnalystResponse,
)
from app.services.analyst_service import answer_question


router = APIRouter(
    prefix="/api/analyst",
    tags=["AI Analyst"],
)


@router.post(
    "/ask",
    response_model=AnalystResponse,
)
def ask_analyst(
    request: AnalystRequest,
    db: Session = Depends(get_db),
):
    return answer_question(
        question=request.question,
        db=db,
    )