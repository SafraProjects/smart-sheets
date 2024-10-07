from fastapi import Depends, HTTPException, status, APIRouter, Body
from fastapi.security import OAuth2PasswordRequestForm

from src.auto.auto_service import AutoService
# from ..auto.auto_controler import app2

from src.application import Access
from .user_service import UserService
from .user.user_model import UserSingUp, UserLogIn, UserDB
from src.auto import Token

# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# auto2_schema = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter(tags=["users"])


@router.post("/sing_up")
async def sing_up(data: UserSingUp) -> UserDB:
    user_in_DB = await UserService.create_user(data)
    return user_in_DB


@router.post("/log_in")
async def log_in(user_data: UserLogIn = Depends()) -> Token:
    token = await UserService.sing_in(user_data=user_data)
    return {"access_token": token}


@router.get("/get_by_id/{id}")
async def test(id: str, user: UserDB = Depends(UserService.get_current_user)) -> dict:
    return {"user": user}


# @router.get("/all")
# async def test() -> dict:
#     return {"hello": id}


# router.include_router(app)
