from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.post("/expenses", response_model=schemas.ExpenseResponse)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    if expense.receipt_id is not None:
        receipt = db.query(models.Receipt).filter(models.Receipt.id == expense.receipt_id).first()
        if not receipt:
            raise HTTPException(status_code=404, detail="Receipt not found")

    new_expense = models.Expense(
        title=expense.title,
        vendor=expense.vendor,
        amount=expense.amount,
        category=expense.category,
        expense_date=expense.expense_date,
        receipt_file_path=expense.receipt_file_path,
        receipt_id=expense.receipt_id
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@router.get("/expenses", response_model=list[schemas.ExpenseResponse])
def get_expenses(
    status: schemas.ExpenseStatus | None = None,
    category: str | None = None,
    vendor: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Expense).options(joinedload(models.Expense.receipt))

    if status:
        query = query.filter(models.Expense.status == status)

    if category:
        query = query.filter(models.Expense.category == category)

    if vendor:
        query = query.filter(models.Expense.vendor == vendor)

    expenses = query.all()
    return expenses


@router.get("/expenses/{expense_id}", response_model=schemas.ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = (
        db.query(models.Expense)
        .options(joinedload(models.Expense.receipt))
        .filter(models.Expense.id == expense_id)
        .first()
    )

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    return expense


@router.put("/expenses/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(expense_id: int, expense_data: schemas.ExpenseUpdate, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense_data.receipt_id is not None:
        receipt = db.query(models.Receipt).filter(models.Receipt.id == expense_data.receipt_id).first()
        if not receipt:
            raise HTTPException(status_code=404, detail="Receipt not found")

    expense.title = expense_data.title
    expense.vendor = expense_data.vendor
    expense.amount = expense_data.amount
    expense.category = expense_data.category
    expense.expense_date = expense_data.expense_date
    expense.receipt_file_path = expense_data.receipt_file_path
    expense.receipt_id = expense_data.receipt_id
    expense.status = expense_data.status

    db.commit()
    db.refresh(expense)

    return expense


@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()

    return {"message": f"Expense {expense_id} deleted successfully"}