import os
import shutil
import uuid

from fastapi import APIRouter, File, UploadFile, HTTPException

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/receipts/upload")
async def upload_receipt(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    file_extension = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    file_id = str(uuid.uuid4())
    saved_filename = f"{file_id}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Receipt uploaded successfully",
        "file_id": file_id,
        "file_path": file_path,
        "original_filename": file.filename
    }