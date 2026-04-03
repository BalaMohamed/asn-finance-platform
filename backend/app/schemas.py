from pydantic import BaseModel
from typing import Optional
from datetime import date

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
    status: str

class ExpenseResponse(BaseModel):
    id: int
    title: str
    vendor: Optional[str] = None
    amount: float
    category: Optional[str] = None
    expense_date: Optional[date] = None
    receipt_file_path: Optional[str] = None
    status: str

    class Config:
        from_attributes = True