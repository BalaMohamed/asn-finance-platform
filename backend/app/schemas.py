from pydantic import BaseModel
from typing import Optional

class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: Optional[str] = None

class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: Optional[str] = None
    status: str

    class Config:
        from_attributes = True