# app/crud/budgets.py

from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.schemas.pydantic import BudgetIn


def create_budget(db: Session, user_id: int, data: BudgetIn):
    budget = Budget(
        category_id=data.category_id,
        amount_limit=data.amount_limit,
        time_period=data.time_period,
        user_id=user_id,
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


def get_budgets_by_user(db: Session, user_id: int):
    return db.query(Budget).filter(Budget.user_id == user_id).all()


def get_budget_by_id(db: Session, budget_id: int, user_id: int):
    return (
        db.query(Budget)
        .filter(Budget.id == budget_id, Budget.user_id == user_id)
        .first()
    )


def update_budget(db: Session, budget_id: int, user_id: int, data: BudgetIn):
    budget = get_budget_by_id(db, budget_id, user_id)
    if not budget:
        return None
    for attr, value in data.dict().items():
        setattr(budget, attr, value)
    db.commit()
    db.refresh(budget)
    return budget


def delete_budget(db: Session, budget_id: int, user_id: int):
    budget = get_budget_by_id(db, budget_id, user_id)
    if not budget:
        return None
    db.delete(budget)
    db.commit()
    return True
