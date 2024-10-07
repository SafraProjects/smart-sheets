from fastapi import Depends, HTTPException, status, APIRouter, Body, Path
from fastapi.security import OAuth2PasswordRequestForm

# >>> models
from src.models import (
    UserSingUp,
    UserLogIn,
    UserDB,
    Token
)

# >>> services
from src.application import Access
from src.dependencies import get_auto_user, get_user_service
from src.users.user.user_service import UserService


router = APIRouter(tags=["Users"])


@router.get("/get_by_id/{id}")
async def test(id: str = Path(...)) -> dict:
    print({"user_id": id})
    user = await UserService.get_user_by_field("_id", id)
    return {"user": user}
