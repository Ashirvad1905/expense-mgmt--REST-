from pydantic import BaseModel, EmailStr
from typing import Optional, List, ForwardRef
from datetime import datetime

# token for jwt
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"



# token for user
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role:Optional[str]='user'

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str  # we'll resolve this from relationship

    class Config:
        from_attributes = True



# category schema
class CategoryIn(BaseModel):
    name: str
    parent_id: Optional[int]

CategoryOut = ForwardRef("CategoryOut")

class CategoryOut(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    children: List["CategoryOut"] = []

    class Config:
        from_attributes = True



# expense schema
class ExpenseIn(BaseModel):
    name:str
    category_id: int
    amount: float
    description: Optional[str]
    is_recurring: bool = False
    date:Optional[datetime]

class ExpenseOut(BaseModel):
    name: str
    id: int
    category_id: int
    amount: float
    description: Optional[str]
    is_recurring: bool
    date: datetime  # ✅ add this if you want it in response
    created_at: datetime

    class Config:
        from_attributes = True




# budget schema
class BudgetIn(BaseModel):
    category_id: int
    amount_limit: float
    time_period: str  # e.g. "2025-06"

class BudgetOut(BaseModel):
    id: int
    category_id: int
    amount_limit: float
    time_period: str

    class Config:
        from_attributes = True



# category out
CategoryOut.model_rebuild()