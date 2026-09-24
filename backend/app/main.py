from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.ingestion import router as ingestion_router
from app.api.classification import router as classification_router
from app.api.transactions import router as transactions_router
from app.api.financial import router as financial_router
from app.api.variance import router as variance_router
from app.api.analyst import router as analyst_router


app = FastAPI(
    title="Finz Financial Review",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingestion_router)
app.include_router(classification_router)
app.include_router(transactions_router)
app.include_router(financial_router)
app.include_router(variance_router)
app.include_router(analyst_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}