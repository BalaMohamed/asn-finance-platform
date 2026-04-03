from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum


class ExpenseStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ExpenseCreate(BaseModel):
    title: str
    vendor: Optional[str] = None
    amount: float
    category: Optional[str] = None
    expense_date: Optional[date] = None
    receipt_file_path: Optional[str] = None
    receipt_id: Optional[int] = None


class ExpenseUpdate(BaseModel):
    title: str
    vendor: Optional[str] = None
    amount: float
    category: Optional[str] = None
    expense_date: Optional[date] = None
    receipt_file_path: Optional[str] = None
    receipt_id: Optional[int] = None
    status: ExpenseStatus


class ExpenseResponse(BaseModel):
    id: int
    title: str
    vendor: Optional[str] = None
    amount: float
    category: Optional[str] = None
    expense_date: Optional[date] = None
    receipt_file_path: Optional[str] = None
    receipt_id: Optional[int] = None
    status: ExpenseStatus

    class Config:
        from_attributes = True


class ReceiptUploadResponse(BaseModel):
    id: int
    original_filename: str | None = None
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

class ReceiptTextExtractionResponse(BaseModel):
    receipt_id: int
    file_path: str
    raw_text: str

class ExpenseDraftResponse(BaseModel):
    title: str
    vendor: str | None = None
    amount: float | None = None
    category: str | None = None
    expense_date: date | None = None
    receipt_id: int

class ExpenseFromReceiptCreateResponse(BaseModel):
    id: int
    title: str
    vendor: str | None = None
    amount: float
    category: str | None = None
    expense_date: date | None = None
    receipt_file_path: str | None = None
    receipt_id: int | None = None
    status: ExpenseStatus

    class Config:
        from_attributes = True

class ExpenseFromReceiptCreateRequest(BaseModel):
    title: str
    vendor: str | None = None
    amount: float
    category: str | None = None
    expense_date: date | None = None