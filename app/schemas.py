from pydantic import BaseModel,EmailStr
from typing import Optional
from pydantic.types import conint
class Post(BaseModel):
    title:str
    content:str
    published:bool= True
class ResponseUser(BaseModel):
    id:int
    email:EmailStr
    class Config:
        orm_mode=True
class Response_post(Post):
     user_id:int
     id:int
     owner:ResponseUser
     class Config:
        orm_mode=True
class createUser(BaseModel):
    email:EmailStr
    password:str
class UserLogin(BaseModel):
    email:EmailStr
    password:str
class Token(BaseModel):
    access_token:str
    token_type:str
class TokenData(BaseModel):
    id:Optional[int] = None
class vote(BaseModel):
    post_id:int
    dir:conint(le=1)