from typing import Optional, Annotated
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str 
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

class PostOut(BaseModel):
    Post: Post
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1)]
