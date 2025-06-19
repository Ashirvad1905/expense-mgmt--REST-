from sqlalchemy.orm import Session
from app.models.category import Category
from fastapi import HTTPException, status
from app.schemas.pydantic import CategoryIn


# Create a new category
def create_category(db: Session, owner_id: int, category_in: CategoryIn):
    category = Category(
        name=category_in.name,
        parent_id=category_in.parent_id,
        owner_id=owner_id
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


# ✅ Get all categories for a user
def get_categories_by_user(db: Session, user_id: int):
    return db.query(Category).filter(Category.owner_id == user_id).all()


# ✅ Get a single category by ID
def get_category(db: Session, category_id: int, user_id: int):
    category = db.query(Category).filter(Category.id == category_id, Category.owner_id == user_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


# ✅ Update a category (name or parent)
def update_category(db: Session, category_id: int, user_id: int, data: CategoryIn):
    category = get_category(db, category_id, user_id)
    category.name = data.name
    category.parent_id = data.parent_id
    db.commit()
    db.refresh(category)
    return category


# ✅ Delete a category
def delete_category(db: Session, category_id: int, user_id: int):
    category = get_category(db, category_id, user_id)
    db.delete(category)
    db.commit()
    return {"detail": "Category deleted"}
