from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, database, token
from ..hash import Hash
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials pass") 
    
    access_token = token.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}