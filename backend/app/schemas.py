from pydantic import BaseModel
from typing import Optional
from datetime import date
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


class ExpenseUpdate(BaseModel):
    title: str
    vendor: Optional[str] = None
    amount: float
    category: Optional[str] = None
    expense_date: Optional[date] = None
    receipt_file_path: Optional[str] = None
    status: ExpenseStatus


class ExpenseResponse(BaseModel):
    id: int
    title: str
    vendor: Optional[str] = None
    amount: float
    category: Optional[str] = None
    expense_date: Optional[date] = None
    receipt_file_path: Optional[str] = None
    status: ExpenseStatus

    class Config:
        from_attributes = True