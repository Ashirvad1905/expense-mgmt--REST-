from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.schemas.pydantic import ExpenseIn


def create_expense(db: Session, user_id: int, data: ExpenseIn):
    expense = Expense(
        name=data.name,
        amount=data.amount,
        description=data.description,
        date=data.date or datetime.now(timezone.utc),  # ✅ timezone-aware
        category_id=data.category_id,
        user_id=user_id,  # ✅ FIXED: 'user_id', not 'owner_id'
        is_recurring=data.is_recurring,
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_expenses_by_user(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).all()  # ✅ 'user_id'


def get_expense_by_id(db: Session, expense_id: int, user_id: int):
    return (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.user_id == user_id)  # ✅ 'user_id'
        .first()
    )


def update_expense(db: Session, expense_id: int, user_id: int, data: ExpenseIn):
    expense = get_expense_by_id(db, expense_id, user_id)
    if not expense:
        return None
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(expense, attr, value)
    db.commit()
    db.refresh(expense)
    return expense


def delete_expense(db: Session, expense_id: int, user_id: int):
    expense = get_expense_by_id(db, expense_id, user_id)
    if not expense:
        return None
    db.delete(expense)
    db.commit()
    return True
