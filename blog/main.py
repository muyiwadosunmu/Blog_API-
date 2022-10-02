from lib2to3.pytree import Base
from fastapi import FastAPI
from . import schemas

app = FastAPI()

@app.post("/post")
def create(post:schemas.Post):
    return post
 