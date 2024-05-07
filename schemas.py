from typing import List
import datetime as _dt
import pydantic as _pydantic
from fastapi import File
from pydantic import Field, EmailStr


class _PostBase(_pydantic.BaseModel):
    title: str = Field(min_length=2, max_length=150)
    description: str = Field(min_length=2, max_length=2000)
    category: str = Field(min_length=2, max_length=100)


class PostCreate(_PostBase):
    image_key: str
    image_url: str


class PostUpdate(_PostBase):
    date_last_updated: _dt.datetime


class Post(_PostBase):
    id: int
    owner_id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime
    image_key: str
    image_url: str

    class Config:
        orm_mode = True


class UserDTO:
    def __init__(self, id, email, username):
        self.id = id
        self.email = email
        self.username = username


class _UserBase(_pydantic.BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=100)


class UserCreate(_UserBase):
    password: str
    confirm_password: str


class UserLogin(_pydantic.BaseModel):
    emailOrUsername: str
    password: str


class User(_UserBase):
    id: int
    posts: List[Post] = []

    class Config:
        orm_mode = True


class UserResponse(_pydantic.BaseModel):
    user: User
    token: str

    class Config:
        orm_mode = True


class ErrorResponse(_pydantic.BaseModel):
    error_message: str
    status_code: int

    def __init__(self, error_message, status_code):
        self.error_message = error_message
        self.status_code = status_code
