from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .auto_model import Token, UserSingUp
from .auto_service import AutoService
from src.models import UserLogIn


router = APIRouter(tags=["Auto"])


@router.post("/sing_up")
async def sing_up(data: UserSingUp):
    verification_data = await AutoService.create_user(data)

    # await Email.send_email_verification(verification_data["Email"], verification_data["VerCode"])

    return {"message": "User registered, please check your email to verify your account"}


# @router.post("/log_in")
# async def log_in(user_data: UserLogIn = Depends()) -> Token:
#     token = await AutoService.sing_in(user_data=user_data)
#     return {"access_token": token}


@router.post("/log-in")
async def login(form_data: UserLogIn = Depends()):
    user = await AutoService.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = AutoService.create_token(user)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/verify-email/{verification_code}")
async def verify_email(verification_code: str):
    return AutoService.verify_token(verification_code)
