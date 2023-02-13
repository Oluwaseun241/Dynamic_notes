from fastapi import APIRouter, status, Depends, HTTPException
from ..database import SessionLocal, engine

router = APIRouter()

db = get_db()

@router.post("/note", status_code=status.HTTP_201_CREATED, tags=["Notes"])
def create_notes(request: schemas.Note, db: Session = Depends(get_db)):
    new_note = models.Note(title=request.title, body=request.body)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get("/note", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowNote], tags=["Notes"])
def show_all(db: Session = Depends(get_db)):
    notes = db.query(models.Note).all()
    return notes


@router.get("/note/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowNote, tags=["Notes"])
def note(id, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Note with id {id} is not available")
    return note


@router.delete("/note/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Notes"])
def delete_note(id, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id ==
                                        id).delete(synchronize_session=False)
    db.commit()

    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Note with id {id} is not available")

    return {"detail": f"Note with id {id} is sucessfully deleted"}


@router.put("/note/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Notes"])
def update_note(id, request: schemas.Note, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Note with id {id} is not available")

    note.title = request.title
    note.body = request.body
    db.commit()
    return {"detail": f"Note with id {id} is sucessfully updated"}
