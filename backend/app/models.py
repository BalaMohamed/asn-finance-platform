from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    expenses = relationship("Expense", back_populates="organization")
    receipts = relationship("Receipt", back_populates="organization")
    members = relationship("OrganizationMember", back_populates="organization")


class OrganizationMember(Base):
    __tablename__ = "organization_members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    organization = relationship("Organization", back_populates="members")


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    expenses = relationship("Expense", back_populates="receipt")
    organization = relationship("Organization", back_populates="receipts")


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
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    status = Column(String, default="pending")
    decision_note = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    receipt = relationship("Receipt", back_populates="expenses")
    organization = relationship("Organization", back_populates="expenses")