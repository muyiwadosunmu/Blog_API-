from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models
from ..hashing import Hash

def create_new_user(request:schemas.User, db:Session):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    if new_user is not None:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)



def show_a_user(user_id:int, db:Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user