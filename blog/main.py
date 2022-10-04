from fastapi import FastAPI, status, HTTPException, Depends
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


@app.post("/post")
def create_post(
    request: schemas.Post,
    db: Session = Depends(get_db),
    status_code=status.HTTP_201_CREATED,
):
    new_post = models.Post(title=request.title, body=request.body)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/post/{post_id}", status_code=status.HTTP_200_OK)
def read_a_posts(post_id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with {post_id} not found",
        )
    return posts





@app.delete("/post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found in DB")
    post.delete(
        synchronize_session=False
    )
    db.commit()
    return "Post deleted"

@app.put("/post/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, request: schemas.Post, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {post_id} not found",
        )
    post.update(dict(request))
    db.commit()
    return "Post Updated Successfully"


@app.get("/posts", response_model=list[schemas.Post], status_code=status.HTTP_200_OK)
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts
