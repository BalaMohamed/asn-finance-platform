from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func
from app.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    vendor = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=True)
    expense_date = Column(Date, nullable=True)
    receipt_file_path = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())