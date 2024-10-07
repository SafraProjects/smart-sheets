from pydantic import BaseModel, EmailStr, Field
from datetime import timedelta
from ..enums.enum_model import UserEnum
from enum import Enum


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    user_name: str
    hash_password: str
    user_type: UserEnum
    expire: timedelta


class UserLogIn(BaseModel):
    name: str
    password: str


class UserSingUp(UserLogIn):
    email: EmailStr


class UserDB(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    email: EmailStr
    hashed_password: str
    user_type: UserEnum = UserEnum.super_admin.value
    active: bool = False

    class Config:
        use_enum_values = True
