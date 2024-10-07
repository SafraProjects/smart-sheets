from pydantic import BaseModel, EmailStr, Field


class UserLogIn(BaseModel):
    name: str
    password: str


class UserSingUp(UserLogIn):
    email: EmailStr
