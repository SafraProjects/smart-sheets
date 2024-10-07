from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from ...enums import UserEnum


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

    @staticmethod
    def convert_UserSingUp_to_user(base_user: UserSingUp, user_id: str) -> "UserDB":
        from ...auto import AutoService
        print(user_id)
        return UserDB(
            _id=user_id,
            name=base_user.name,
            email=base_user.email,
            hashed_password=AutoService.get_hash_password(
                base_user.password)
        )
