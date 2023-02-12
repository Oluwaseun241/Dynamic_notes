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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/note", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowNote], tags=["Notes"])
def show_all(db: Session = Depends(get_db)):
    notes = db.query(models.Note).all()
    return notes


@app.get("/note/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowNote, tags=["Notes"])
def note(id, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Note with id {id} is not available")
    return note


@app.post("/note", status_code=status.HTTP_201_CREATED, tags=["Notes"])
def create_notes(request: schemas.Note, db: Session = Depends(get_db)):
    new_note = models.Note(title=request.title, body=request.body)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@app.delete("/note/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Notes"])
def delete_note(id, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id ==
                                        id).delete(synchronize_session=False)
    db.commit()

    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Note with id {id} is not available")

    return {"detail": f"Note with id {id} is sucessfully deleted"}


@app.put("/note/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Notes"])
def update_note(id, request: schemas.Note, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Note with id {id} is not available")

    note.title = request.title
    note.body = request.body
    db.commit()
    return {"detail": f"Note with id {id} is sucessfully updated"}


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
