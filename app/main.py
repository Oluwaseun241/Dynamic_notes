from fastapi import FastAPI, Depends, status, HTTPException
from typing import List
from . import schemas, models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/note", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowNote])
def show_all(db: Session = Depends(get_db)):
    notes = db.query(models.Note).all()
    return notes


@app.get("/note/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowNote)
def note(id, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Note with id {id} is not available")


    return note


@app.post("/note", status_code=status.HTTP_201_CREATED)
def create_notes(request: schemas.Note, db: Session = Depends(get_db)):
    new_note = models.Note(title=request.title, body=request.body)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@app.delete("/note/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_note(id, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == id).delete(synchronize_session=False)
    db.commit()


    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Note with id {id} is not available")

    return {"detail": f"Note with id {id} is sucessfully deleted"}

   
@app.put("/note/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_note(id, request: schemas.Note, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Note with id {id} is not available")
    
    note.title = request.title
    note.body = request.body
    db.commit()
    return {"detail": f"Note with id {id} is sucessfully updated"}


@app.post("/user")
def create_user(request : schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(username=request.username,email=request.email,password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user