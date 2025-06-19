# app/api/routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token, decode_access_token
from app.crud import budgets, categories, expenses, users
from app.db.session import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.pydantic import *

router = APIRouter()

# ✅ Add OAuth2 scheme to extract token from Authorization header
oauth2_scheme = HTTPBearer()

# ========== AUTH ROUTES ==========


@router.post("/signup", response_model=UserOut, tags=["Auth"])
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    user = users.create_user(db, user_in, role_name=user_in.role or "user")
    user.role = user.role.name
    return user


@router.post("/login", response_model=Token, tags=["Auth"])
def login(data: UserCreate, db: Session = Depends(get_db)):
    user = users.authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


# ========== UTILITY ==========


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials  # ✅ Extract actual token string
    try:
        payload = decode_access_token(token)
        user = users.get_user_by_email(db, payload["sub"])
        if not user:
            raise Exception()
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ========== CATEGORIES ==========


@router.post("/categories", response_model=CategoryOut, tags=["Categories"])
def create_category_view(
    data: CategoryIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return categories.create_category(db, current_user.id, data)


@router.get("/categories", response_model=list[CategoryOut], tags=["Categories"])
def get_categories_view(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return categories.get_categories_by_user(db, current_user.id)


@router.put("/categories/{cat_id}", response_model=CategoryOut, tags=["Categories"])
def update_category_view(
    cat_id: int,
    data: CategoryIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return categories.update_category(db, cat_id, current_user.id, data)


@router.delete("/categories/{cat_id}", tags=["Categories"])
def delete_category_view(
    cat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return categories.delete_category(db, cat_id, current_user.id)


# ============Expenses=======================
@router.post("/expenses", response_model=ExpenseOut, tags=["Expenses"])
def create_expense(
    data: ExpenseIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return expenses.create_expense(db, current_user.id, data)


@router.get("/expenses", response_model=list[ExpenseOut], tags=["Expenses"])
def list_expenses(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return expenses.get_expenses_by_user(db, current_user.id)


@router.get("/expenses/{expense_id}", response_model=ExpenseOut, tags=["Expenses"])
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    expense = expenses.get_expense_by_id(db, expense_id, current_user.id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/expenses/{expense_id}", response_model=ExpenseOut, tags=["Expenses"])
def update_expense(
    expense_id: int,
    data: ExpenseIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    expense = expenses.update_expense(db, expense_id, current_user.id, data)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.delete("/expenses/{expense_id}", tags=["Expenses"])
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = expenses.delete_expense(db, expense_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted"}


# ================Budgets=================================


@router.post("/budgets", response_model=BudgetOut, tags=["Budgets"])
def create_budget(
    data: BudgetIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return budgets.create_budget(db, current_user.id, data)


@router.get("/budgets", response_model=list[BudgetOut], tags=["Budgets"])
def list_budgets(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return budgets.get_budgets_by_user(db, current_user.id)


@router.get("/budgets/{budget_id}", response_model=BudgetOut, tags=["Budgets"])
def get_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    budget = budgets.get_budget_by_id(db, budget_id, current_user.id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


@router.put("/budgets/{budget_id}", response_model=BudgetOut, tags=["Budgets"])
def update_budget(
    budget_id: int,
    data: BudgetIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    budget = budgets.update_budget(db, budget_id, current_user.id, data)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


@router.delete("/budgets/{budget_id}", tags=["Budgets"])
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = budgets.delete_budget(db, budget_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Budget not found")
    return {"message": "Budget deleted"}


@router.get("/debug/users", tags=["Debug"])
def get_all_users_debug(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/debug/categories", tags=["Debug"])
def view_all_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()
