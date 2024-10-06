from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from ..enums import UserEnum


class UserSing(BaseModel):
    name: str
    password: str


class BaseUser(UserSing):
    email: EmailStr


class UserDB(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    email: EmailStr
    hashed_password: str
    user_type: UserEnum = UserEnum.super_admin.value
    active: bool = False

    @staticmethod
    def convert_baseuser_to_user(base_user: BaseUser, user_id: str) -> "UserDB":
        from ..auto import AutoUser
        print(user_id)
        return UserDB(
            _id=user_id,
            name=base_user.name,
            email=base_user.email,
            hashed_password=AutoUser.get_hash_password(
                base_user.password)
        )
