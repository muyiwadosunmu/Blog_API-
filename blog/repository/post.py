from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models

def get_all_post(db:Session):
    posts = db.query(models.Post).all()
    return posts

def create_a_post(request:schemas.Post, db:Session):
    new_post = models.Post(title=request.title, body=request.body, user_id=1)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def delete_a_post(post_id:int, db:Session):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Content not found in DB"
        )
    post.delete(synchronize_session=False)
    db.commit()
    return "Post deleted"

def update_a_post(post_id:int,request:schemas.Post, db:Session):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {post_id} not found",
        )
    post.update(dict(request))
    db.commit()
    return post

def show_a_post(post_id:int,db:Session):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with {post_id} not found",
        )
    return post