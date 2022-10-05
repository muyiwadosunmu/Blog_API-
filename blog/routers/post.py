from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from .. import schemas, models, database
from sqlalchemy.orm import Session


router = APIRouter()
get_db = database.get_db

@router.get(
    "/posts",
    tags=["posts"],
    response_model=List[schemas.ShowPost],
    status_code=status.HTTP_200_OK,
)
def read_posts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/post", tags=["posts"], status_code=status.HTTP_201_CREATED)
def create_post(
    request: schemas.Post,
    db: Session = Depends(get_db),
):
    new_post = models.Post(title=request.title, body=request.body, user_id=1)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete(
    "/post/{post_id}", tags=["posts"], status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Content not found in DB"
        )
    post.delete(synchronize_session=False)
    db.commit()
    return "Post deleted"


@router.put("/post/{post_id}", tags=["posts"], status_code=status.HTTP_202_ACCEPTED)
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


@router.get(
    "/post/{post_id}",
    tags=["posts"],
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowPost,
)
def read_a_post(post_id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with {post_id} not found",
        )
    return posts