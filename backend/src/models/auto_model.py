from pydantic import BaseModel, EmailStr, Field
from datetime import timedelta
from .Enums import UserEnum


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    user_name: str
    hash_password: str
    user_type: UserEnum
    expire: timedelta
