from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, database
from ..hash import Hash
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not Hash.verify_password(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials pass") 
    return user
