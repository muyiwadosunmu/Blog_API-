from typing import List, Optional
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True

class Post(PostBase):
    class Config:
        orm_mode = True

class ShowUser(BaseModel):
    name: str
    email: str
    posts : list[Post]

    class Config:
        orm_mode = True



class ShowPost(BaseModel):
    title: str
    body: str
    creator: ShowUser 

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password:str

