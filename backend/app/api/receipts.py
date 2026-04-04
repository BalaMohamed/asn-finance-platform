import os
import shutil
import uuid

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.services.ocr import extract_text_from_image

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/receipts/upload", response_model=schemas.ReceiptUploadResponse)
async def upload_receipt(organization_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
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
        file_path=file_path,
        organization_id=organization_id
    )

    db.add(new_receipt)
    db.commit()
    db.refresh(new_receipt)

    return new_receipt


@router.get("/receipts/{receipt_id}/extract-text", response_model=schemas.ReceiptTextExtractionResponse)
def extract_receipt_text(receipt_id: int, db: Session = Depends(get_db)):
    receipt = db.query(models.Receipt).filter(models.Receipt.id == receipt_id).first()

    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    if not os.path.exists(receipt.file_path):
        raise HTTPException(status_code=404, detail="Receipt file not found on disk")

    raw_text = extract_text_from_image(receipt.file_path)

    return {
        "receipt_id": receipt.id,
        "file_path": receipt.file_path,
        "raw_text": raw_text
    }

@router.post("/receipts/{receipt_id}/create-expense-draft", response_model=schemas.ExpenseDraftResponse)
def create_expense_draft(receipt_id: int, db: Session = Depends(get_db)):
    receipt = db.query(models.Receipt).filter(models.Receipt.id == receipt_id).first()

    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    # Simulated extraction (for now)
    return {
        "title": "New Expense",
        "vendor": "Unknown Vendor",
        "amount": None,
        "category": None,
        "expense_date": None,
        "receipt_id": receipt.id
    }

@router.post(
    "/receipts/{receipt_id}/create-expense",
    response_model=schemas.ExpenseFromReceiptCreateResponse
)
def create_expense_from_receipt(
    receipt_id: int,
    expense_data: schemas.ExpenseFromReceiptCreateRequest,
    db: Session = Depends(get_db)
):
    receipt = db.query(models.Receipt).filter(models.Receipt.id == receipt_id).first()

    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    new_expense = models.Expense(
        title=expense_data.title,
        vendor=expense_data.vendor,
        amount=expense_data.amount,
        category=expense_data.category,
        expense_date=expense_data.expense_date,
        receipt_file_path=receipt.file_path,
        receipt_id=receipt.id,
        organization_id=receipt.organization_id,
        status="pending"
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense

@router.get("/receipts", response_model=list[schemas.ReceiptResponse])
def get_receipts(db: Session = Depends(get_db)):
    receipts = db.query(models.Receipt).order_by(models.Receipt.uploaded_at.desc()).all()
    return receipts


@router.get("/receipts/{receipt_id}", response_model=schemas.ReceiptResponse)
def get_receipt(receipt_id: int, db: Session = Depends(get_db)):
    receipt = db.query(models.Receipt).filter(models.Receipt.id == receipt_id).first()

    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    return receipt

@router.delete("/receipts/{receipt_id}")
def delete_receipt(receipt_id: int, db: Session = Depends(get_db)):
    receipt = db.query(models.Receipt).filter(models.Receipt.id == receipt_id).first()

    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    linked_expense = db.query(models.Expense).filter(models.Expense.receipt_id == receipt_id).first()
    if linked_expense:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete receipt because it is linked to an expense"
        )

    if os.path.exists(receipt.file_path):
        os.remove(receipt.file_path)

    db.delete(receipt)
    db.commit()

    return {"message": f"Receipt {receipt_id} deleted successfully"}