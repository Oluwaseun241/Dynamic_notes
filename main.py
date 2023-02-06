from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Note(BaseModel):
    # id: int
    title: str
    body: str


@app.get("/")
def notes():
    return 'Hello world'

@app.post("/blog")
def create_notes(request: Note):
    return f'Blog created {request.title}'