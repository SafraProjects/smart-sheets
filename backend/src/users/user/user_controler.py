from fastapi import Depends, HTTPException, Request, Response, status, APIRouter, Body, Path
from fastapi.security import OAuth2PasswordRequestForm

# >>> models
from src.models import (
    UserSingUp,
    UserLogIn,
    UserDB,
    Token
)

# >>> services
from src.application import Env
from .user_service import UserService
import src.auto.auto_service as Auto


router = APIRouter(tags=["Users"])


@router.get("/get_by_id/{id}")
@Auto.authenticate_user
async def test(request: Request, response: Response, id: str = Path(...),) -> dict:
    print({"user_id": id})
    user = await UserService.get_user_by_field("_id", id)
    return {"user": user}
