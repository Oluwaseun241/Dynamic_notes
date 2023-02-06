from fastapi import FastAPI, Depends, status, HTTPException
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


@app.get("/blog", status_code=status.HTTP_200_OK)
def show_all(db: Session = Depends(get_db)):
    notes = db.query(models.Note).all()
    return notes


@app.get("/blog{id}", status_code=status.HTTP_200_OK)
def note(id, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Note with id {id} is not available")


    return note


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_notes(request: schemas.Note, db: Session = Depends(get_db)):
    new_note = models.Note(title=request.title, body=request.body)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.put("/blog{id}")
def update_note():
    return 'done'