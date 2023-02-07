from pydantic import BaseModel

class Note(BaseModel):
    title: str
    body: str

class ShowNote(Note):
    class Config():
        orm_mode = True