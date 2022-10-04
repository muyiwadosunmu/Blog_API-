from pydantic import BaseModel


class Post(BaseModel):
    title:str
    body:str

    class Config:
        orm_mode=True