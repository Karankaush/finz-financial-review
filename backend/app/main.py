from fastapi import FastAPI

from app.api.ingestion import router as ingestion_router
from app.api.classification import router as classification_router
from app.api.transactions import router as transactions_router
from app.api.financial import router as financial_router
from app.api.variance import router as variance_router


app = FastAPI(
    title="Finz Financial Review",
    version="1.0.0",
)

app.include_router(ingestion_router)
app.include_router(classification_router)
app.include_router(transactions_router)
app.include_router(financial_router)
app.include_router(variance_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}