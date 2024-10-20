from fastapi import Depends
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from .Enums import UserEnum
from .user import UserSingUp


class UserDB(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: EmailStr
    hashed_password: str
    user_type: UserEnum = UserEnum.user.value
    active: bool = False

    @staticmethod
    def convert_base_user_to_userDB(user_base: UserSingUp, user_id: str, hash_pw: str):
        return UserDB(
            id=user_id,
            name=user_base.name,
            email=user_base.email,
            hashed_password=hash_pw,
        )


class UserFront(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: EmailStr
    user_type: UserEnum

    @staticmethod
    def convert_userDB_to_UserFront(user: UserDB):
        return UserFront(
            id=user.id,
            name=user.name,
            email=user.email,
            user_type=user.user_type.value)
