from fastapi import FastAPI, Depends
from . import schemas, models
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from blog import database

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/posts", response_model=list[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts


@app.post("/post")
def create_post(request: schemas.Post, db: Session = Depends(get_db)):
    new_post = models.Post(title=request.title, body=request.body)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{post_id}", response_model=schemas.Post)
def read_a_posts(post_id:int, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.post_id == post_id).first()
    return posts
