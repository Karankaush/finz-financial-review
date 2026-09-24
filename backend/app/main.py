from fastapi import FastAPI

from app.api.ingestion import router as ingestion_router
from app.api.classification import router as classification_router


app = FastAPI(
    title="Finz Financial Review",
    version="1.0.0",
)

app.include_router(ingestion_router)
app.include_router(classification_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}