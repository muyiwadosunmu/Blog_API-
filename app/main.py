from fastapi import FastAPI
from blog import models
from blog.database import engine
from blog.routers import post, user, authentication


app = FastAPI(
    title="FMy Blog API",
    description="A blog API with oauth2 authentication, user system e.t.c ",
    version="0.0.1",
    contact={
        "name": "Muyiwa.rs",
        "email": "oluwamuyiwadosunmu@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
)

models.Base.metadata.create_all(engine)

# Routes
app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
