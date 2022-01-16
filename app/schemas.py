from turtle import st
from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

from app.database import Base

class PostBase(BaseModel) :
    title : str
    content : str
    published : bool = True

class PostCreate(PostBase) :
    pass

class UserOut(BaseModel) :
    id : int
    email : EmailStr
    created_at : datetime
    
    class Config :
        orm_mode = True

class Post(PostBase) :
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut
    class Config :
        orm_mode = True

class PostOut(BaseModel) :
    Post : Post
    votes : int


class UserCreate(BaseModel) :
    email : EmailStr
    password : str



class UserLogin(UserCreate) :
    pass

class Token(BaseModel) :
    access_token : str
    token_type : str

class TokenData(BaseModel) :
    id : int

class Vote(BaseModel) :
    post_id : int
    dir : bool