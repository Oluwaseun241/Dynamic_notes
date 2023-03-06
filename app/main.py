from fastapi import FastAPI
from . import schemas, models
from .database import SessionLocal, engine
from app.routers import notes, users, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dynamic Notes",
    description='A simple User CRUD API built with FastAPI and SQLAlchemy',
    version="0.1.0",
    contact={
        "name": "Oluwaseun",
        "url": "https://github.com/Oluwaseun241",
    },
)
app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(users.router)

