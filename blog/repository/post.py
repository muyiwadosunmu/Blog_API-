from sqlalchemy.orm import Session
from .. import schemas, models

def get_all_post(db:Session):
    posts = db.query(models.Post).all()
    return posts