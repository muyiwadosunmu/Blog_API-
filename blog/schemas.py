from pydantic import BaseModel


class Post(BaseModel):
    id: int
    title: str
    body: str


class ShowPost(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True

class User(BaseModel):
    name:str
    email:str
    password:str

    class Config:
        orm_mode = True