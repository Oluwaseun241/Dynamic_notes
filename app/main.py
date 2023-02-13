from fastapi import FastAPI, Depends, status, HTTPException
from typing import List
from . import schemas, models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .hash import Hash


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


@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=["Users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    user_with_username = db.query(models.User).filter(
        models.User.username == request.username).first()
    user_with_email = db.query(models.User).filter(
        models.User.email == request.email).first()

    if user_with_username or user_with_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username or email already used")

    hashed_password = Hash.get_password_hash(request.password)
    new_user = models.User(username=request.username,
                           email=request.email, password=hashed_password)

    db.add(new_user)
    db.commit()

    return new_user


@app.get("/user/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=["Users"])
def user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} is not available")
    return user
