from pydantic import BaseModel, EmailStr, Field


class UserLogIn(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6, max_length=12)


class UserSingUp(BaseModel):
    name: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=12)
