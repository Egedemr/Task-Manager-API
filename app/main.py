from fastapi import FastAPI
from app.db.database import engine
from app.db.base import Base
from app.models import user, task

app = FastAPI(title="Task Manager API")
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Task Manager API is running"}
