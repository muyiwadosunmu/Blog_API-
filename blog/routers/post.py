from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from .. import schemas, models, database
from sqlalchemy.orm import Session
from ..repository import post

router = APIRouter(tags=["Posts"])
get_db = database.get_db


@router.get(
    "/posts",
    response_model=List[schemas.ShowPost],
    status_code=status.HTTP_200_OK,
)
def read_posts(db: Session = Depends(database.get_db)):
    return post.get_all_post(db)


@router.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(request: schemas.Post, db: Session = Depends(get_db)):
    return post.create_a_post(request, db)


@router.delete("/post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Content not found in DB"
        )
    post.delete(synchronize_session=False)
    db.commit()
    return "Post deleted"


@router.put("/post/{post_id}", status_code=status.HTTP_202_ACCEPTED)
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
