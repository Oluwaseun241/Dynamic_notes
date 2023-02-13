from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, database

router = APIRouter(
    prefix="/note",
    tags=['Notes']
)

get_db = database.get_db

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_notes(request: schemas.Note, db: Session = Depends(get_db)):
    new_note = models.Note(title=request.title, body=request.body)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowNote])
def show_all(db: Session = Depends(get_db)):
    notes = db.query(models.Note).all()
    return notes


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowNote)
def note(id, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Note with id {id} is not available")
    return note


@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_note(id, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id ==
                                        id).delete(synchronize_session=False)
    db.commit()

    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Note with id {id} is not available")

    return {"detail": f"Note with id {id} is sucessfully deleted"}


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_note(id, request: schemas.Note, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Note with id {id} is not available")

    note.title = request.title
    note.body = request.body
    db.commit()
    return {"detail": f"Note with id {id} is sucessfully updated"}
