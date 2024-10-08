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
    user_type: UserEnum = UserEnum.user
    active: bool = False

    @staticmethod
    def convert_base_user_to_userDB(user_base: UserSingUp, user_id: str, hash_pw: str):
        return UserDB(
            _id=user_id,
            name=user_base.name,
            email=user_base.email,
            hashed_password=hash_pw,
        )
