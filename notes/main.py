from fastapi import FastAPI
from . import schemas


app = FastAPI()


@app.get("/")
def notes():
    return 'all'

@app.post("/blog")
def create_notes(request: schemas.Note):
    return f'Blog created {request.title}'