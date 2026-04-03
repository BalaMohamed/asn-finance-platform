from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    expenses = relationship("Expense", back_populates="receipt")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    vendor = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=True)
    expense_date = Column(Date, nullable=True)
    receipt_file_path = Column(String, nullable=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id"), nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    receipt = relationship("Receipt", back_populates="expenses")