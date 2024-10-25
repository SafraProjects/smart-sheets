from pydantic import BaseModel, EmailStr, Field
from .Enums import UserEnum


class UserLogIn(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6, max_length=12)


class UserSingUp(BaseModel):
    name: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=12)


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
            _id=user_id,
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
            _id=user.id,
            name=user.name,
            email=user.email,
            user_type=user.user_type.value)
