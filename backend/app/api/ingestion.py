from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.database import get_db
from schemas.ingestion import IngestionResponse
from app.services.ingestion_service import ingest_transactions


router = APIRouter(
    prefix="/api/ingestion",
    tags=["Ingestion"],
)


@router.post(
    "/transactions",
    response_model=IngestionResponse,
)
async def upload_transactions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is required",
        )

    if not file.filename.lower().endswith(
        (".xlsx", ".xls", ".csv")
    ):
        raise HTTPException(
            status_code=400,
            detail="Only Excel or CSV files are supported",
        )

    try:
        content = await file.read()

        count = ingest_transactions(
            content,
            db,
        )

        return IngestionResponse(
            message="Transactions ingested successfully",
            total_transactions=count,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )