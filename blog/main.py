from fastapi import FastAPI, status, HTTPException, Depends
from . import schemas, models
from sqlalchemy.orm import Session
from .database import engine, get_db 
from  .routers import post, user
from blog import database
from . hashing import Hash
from .routers import post, user


app = FastAPI() 



app.include_router(post.router)

models.Base.metadata.create_all(engine)

get_db = database.get_db





@app.get(
    "/post/{post_id}",
    tags=["posts"],
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowPost,
)
def read_a_posts(post_id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with {post_id} not found",
        )
    return posts


@app.delete(
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


@app.post("/post/{post_id}", tags=["posts"], status_code=status.HTTP_202_ACCEPTED)
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


@app.post(
    "/user",
    tags=["users"],
    response_model=schemas.ShowUser,
    status_code=status.HTTP_201_CREATED,
)
def create_user(request: schemas.User, db: Session = Depends(get_db)):

    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{user_id}",tags=["users"],response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
def get_a_user(user_id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user