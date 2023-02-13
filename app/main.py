from fastapi import FastAPI
from . import schemas, models
from .database import SessionLocal, engine
from app.routers import notes, users


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    # title="Dynamic Notes",
    # description='A simple User CRUD API built with FastAPI and SQLAlchemy',
    # version="0.0.9",
    # contact={
    #     "name": "Oluwaseun",
    #     "url": "https://github.com/Oluwaseun241",
    #     "email": "tanimolaoluwaseun70@gmail.com",
    # },
)

app.include_router(notes.router)
app.include_router(users.router)

