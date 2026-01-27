from fastapi import FastAPI

from app.db.database import engine
from app.db.base import Base
from app.models import user, task  # noqa: F401
from app.api.auth import router as auth_router

app = FastAPI(title="Task Manager API")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Task Manager API is running"}