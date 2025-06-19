# app/models/budget.py
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    amount_limit = Column(Float, nullable=False)
    time_period = Column(String, nullable=False)  # format: "2025-06"

    user = relationship("User", back_populates="budgets")
    category = relationship("Category")
