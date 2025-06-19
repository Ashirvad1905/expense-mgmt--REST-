from fastapi import FastAPI
from app.db.session import Base, engine
from app.models import user, role, category, expense, budget
from app.api.routes import router as api_router
from app.models.role import Role, RoleEnum
from app.db.session import SessionLocal

app = FastAPI()

Base.metadata.create_all(bind=engine)

db = SessionLocal()
for r in RoleEnum:
    if not db.query(Role).filter_by(name=r).first():
        db.add(Role(name=r))
db.commit()
db.close()

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}
