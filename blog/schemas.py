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
