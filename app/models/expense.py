# app/models/expense.py

from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.session import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    name = Column(String, nullable=False)  # ✅ user-friendly name field

    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    receipt_url = Column(String, nullable=True)
    is_recurring = Column(Boolean, default=False)

    # ✅ Add this field to store the actual date of the expense
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")
