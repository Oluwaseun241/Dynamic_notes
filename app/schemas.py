from typing import List
from pydantic import BaseModel

class Note(BaseModel):
    title: str
    body: str

    class Config():
        orm_mode = True

class ShowUser(BaseModel):
    username: str
    email: str
    notes: List[Note] = []
    
    class Config():
        orm_mode = True

class ShowNote(BaseModel):
    title: str
    body: str
    owner: ShowUser
    
    class Config():
        orm_mode = True

class User(BaseModel):
    username: str
    email: str
    password: str