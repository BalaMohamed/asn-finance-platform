import os
import shutil
import uuid

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/receipts/upload", response_model=schemas.ReceiptUploadResponse)
async def upload_receipt(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    file_extension = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    file_id = str(uuid.uuid4())
    saved_filename = f"{file_id}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_receipt = models.Receipt(
        original_filename=file.filename,
        file_path=file_path
    )

    db.add(new_receipt)
    db.commit()
    db.refresh(new_receipt)

    return new_receipt