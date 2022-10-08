from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from blog import schemas, models, database, oauth2
from sqlalchemy.orm import Session
from blog.repository import post


router = APIRouter(tags=["Posts"])
get_db = database.get_db


@router.get(
    "/posts",
    response_model=List[schemas.ShowPost],
    status_code=status.HTTP_200_OK,
)
def read_posts(db: Session = Depends(database.get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
    return post.get_all_post(db)


@router.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(request: schemas.Post, db: Session = Depends(get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
    return post.create_a_post(request, db)


@router.delete("/post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user:schemas.User=Depends(oauth2.get_current_user)):
    return post.delete_a_post(post_id,db)


@router.put("/post/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, request: schemas.Post, db: Session = Depends(get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
    return post.update_a_post(post_id, request, db)


@router.get(
    "/post/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowPost,
)
def read_a_post(post_id: int, db: Session = Depends(get_db), current_user:schemas.User=Depends(oauth2.get_current_user)):
    return post.show_a_post(id, db)
