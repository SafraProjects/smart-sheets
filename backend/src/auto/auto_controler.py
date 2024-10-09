from fastapi import APIRouter, Depends, Header, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# >>> models
from src.models import UserLogIn, Token, UserSingUp

# >>> services
from .auto_service import AutoService, authenticate_login
from services.email.email_service import EmailService
from src.application import Access


router = APIRouter(tags=["Auto"])


# >>> sing up


@router.post("/sing-up")
async def sing_up(data: UserSingUp = Depends()):
    verification_data = await AutoService.create_user(data)
    url = Access.get_backend_port() + "/auto/verify-email/" + \
        verification_data["VerCode"]

    EmailService.send_email(
        receiver_email=verification_data["Email"],
        body=[
            "ברוך הבא לאתר Tabio",
            "",
            "האתר שבו תוכל למנף קבצי רשומות לנקסט לבל :)",
            "לפני שמתחילים..."
        ],
        link=url
    )
    return {"message": "User registered, please check your email to verify your account"}


@router.post("/resend-verification-email/{user_email}")
async def verify_email(user_email: str):
    token = AutoService.create_verification_token(
        user_email=user_email)

    url = Access.get_backend_port() + "/auto/verify-email/" + token
    EmailService.send_email(
        receiver_email=user_email,
        body=[
            "ברוך שובך לאתר Tabio",
            "",
            "לפני שמתחילים..."
        ],
        link=url
    )
    return {"message": "User registered, please check your email to verify your account"}


@router.get("/verify-email/{verification_code}")
async def verify_email(verification_code: str):
    print(verification_code)
    return await AutoService.verify_account(verification_code)


# >>> Login


@router.post("/log-in")
@authenticate_login
async def login(request: Request, response: Response, form_data: UserLogIn = Depends()):

    user = await AutoService.authenticate(email=form_data.email, password=form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token, user_type = AutoService.create_access_token(user)
    refresh_token = AutoService.create_refresh_token(user)

    response.set_cookie(key="access_token",
                        value=access_token, httponly=True, secure=True)
    response.set_cookie(key="refresh_token",
                        value=refresh_token, httponly=True, secure=True)

    return {"message": "Login successful"}


# @router.post("/refresh-token")
# async def refresh_token(request: Request, response: Response):
#     refresh_token = request.cookies.get("refresh_token")
#     if not refresh_token:
#         raise HTTPException(
#             status_code=403, detail="No refresh token available")

#     new_access_token = AutoService.verify_refresh_token(refresh_token)
#     if not new_access_token:
#         raise HTTPException(
#             status_code=403, detail="Invalid or expired refresh token")

#     response.set_cookie(key="access_token",
#                         value=new_access_token, httponly=True, secure=True)

#     return {"message": "Token refreshed"}


# @router.get("/auto-login")
# async def auto_login(request: Request):
#     access_token = request.cookies.get("access_token")
#     refresh_token = request.cookies.get("refresh_token")

#     if access_token:
#         payload = AutoService.verify_access_token(access_token)
#         if payload:
#             return {"message": "User is already logged in"}

#     if refresh_token:
#         new_access_token = AutoService.refresh_access_token(refresh_token)
#         return {"access_token": new_access_token, "message": "Auto login successful"}

#     raise HTTPException(status_code=401, detail="Login required")
