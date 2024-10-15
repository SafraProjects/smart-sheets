from fastapi import APIRouter, Body, Depends, Header, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# >>> models
from src.models import UserLogIn, Token, UserSingUp

# >>> services
from .auto_service import AutoService, authenticate_login
from services.email.email_service import EmailService
from services.application import Env


router = APIRouter(tags=["Auto"])


# >>> sing in


@router.post("/sign-in")
async def sing_up(data: UserSingUp):
    verification_data = await AutoService.create_user(data)
    url = Env.get_frontend_port() + "/auto/verify/" + \
        verification_data["VerCode"] + "/" + verification_data["Email"]

    EmailService.send_email(
        receiver_email=verification_data["Email"],
        body=[
            data.name + " ברוך הבא לאתר Tabio",
            "",
            "האתר שבו תוכל למנף קבצי רשומות לנקסט לבל :)",
            "לפני שמתחילים..."
        ],
        link=url
    )
    print("\n\033[92m email send :\033[0m")
    return {"message": "User registered, please check your email to verify your account"}


@router.post("/resend-verification-email/{user_email}")
async def verify_email(user_email: str):
    token = AutoService.create_verification_token(
        user_email=user_email)

    url = Env.get_frontend_port() + "/auto/verify/" + token
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


@router.post("/verify-email/{verification_code}")
async def verify_email(verification_code: str):
    print(verification_code)
    return await AutoService.verify_account(verification_code)


@router.post("/send-verification-password/{user_email}")
async def verify_email(user_email: str):
    code = AutoService.generate_code(4)
    message = await AutoService.set_verification_password(user_email=user_email, code=str(code))
    EmailService.send_email(
        receiver_email=user_email,
        body=[
            "ברוך שובך לאתר Tabio",
            "",
            "קוד האימות שלך הוא: <b>" + str(code) + "</b>"
        ],
    )
    return {"message": "User registered, please check your email to verify your account, " + message["message"]}


@router.post("/verify-password/{user_email}/{verification_code}")
async def verify_temp_password(user_email: str, verification_code: str):
    return await AutoService.verify_temp_password(user_email=user_email, code=verification_code)


@router.post("/update-password/{user_email}/{new_password}")
async def update_password(user_email: str, new_password: str):
    return await AutoService.update_user_password(user_email=user_email, code=new_password)

# >>> Login


@router.post("/log-in")
@authenticate_login
async def login(request: Request, response: Response, form_data: UserLogIn):
    print("aca")
    user = await AutoService.authenticate(email=form_data.email, password=form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = AutoService.create_access_token(user)
    refresh_token = AutoService.create_refresh_token(user)

    response.set_cookie(key="access_token",
                        value=access_token, httponly=True, secure=True)
    response.set_cookie(key="refresh_token",
                        value=refresh_token, httponly=True, secure=True)

    return user


@router.get("/auto-login")
@authenticate_login
async def auto_login():
    raise HTTPException(status_code=401, detail="Login required")
