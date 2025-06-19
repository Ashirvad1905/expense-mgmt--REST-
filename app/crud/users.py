from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.role import Role
from app.models.user import User
from app.schemas.pydantic import UserCreate


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user_in: UserCreate, role_name: str = "user"):
    if get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise HTTPException(status_code=400, detail=f"Role '{role_name}' not found")

    user = User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role_id=role.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
