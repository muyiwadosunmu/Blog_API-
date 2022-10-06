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