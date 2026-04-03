from fastapi import FastAPI

from app.database import engine, Base
from app import models
from app.api.expenses import router as expenses_router
from app.api.receipts import router as receipts_router

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "ASN Finance API is running"}


app.include_router(expenses_router)
app.include_router(receipts_router)