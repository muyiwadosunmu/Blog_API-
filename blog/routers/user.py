from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from .. import schemas, models, database
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..repository import user


router = APIRouter(prefix="/user", tags=["Users"])

get_db = database.get_db


@router.post(
    "/",
    response_model=schemas.ShowUser,
    status_code=status.HTTP_201_CREATED,
)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = user.create_new_user(request, db)
    return new_user


@router.get(
    "/{user_id}", response_model=schemas.ShowUser, status_code=status.HTTP_200_OK
)
def get_a_user(user_id: int, db: Session = Depends(get_db)):
    a_user = user.show_a_user(user_id, db)
    return a_user
 