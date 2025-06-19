# app/models/role.py
import enum

from sqlalchemy import Column, Enum, Integer
from sqlalchemy.orm import relationship

from app.db.session import Base


class RoleEnum(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    user = "user"


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(RoleEnum), unique=True, nullable=False)

    users = relationship("User", back_populates="role")
