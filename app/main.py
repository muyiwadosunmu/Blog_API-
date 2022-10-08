from fastapi import FastAPI
from blog import models
from blog.database import engine
from blog.routers import post, user, authentication


app = FastAPI()

models.Base.metadata.create_all(engine)

# Routes
app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)


