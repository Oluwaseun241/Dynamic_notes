from pydantic import BaseModel

class Note(BaseModel):
    title: str
    body: str

class ShowNote(Note):
    class Config():
        orm_mode = True

class User(BaseModel):
    username: str
    email: str
    password: str

class ShowUser(BaseModel):
    username: str
    email: str
    
    class Config():
        orm_mode = True
    