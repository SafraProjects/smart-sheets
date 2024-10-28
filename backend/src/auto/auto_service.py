from fastapi import Depends, status, HTTPException, Request, Response
# from fastapi.responses import RedirectResponse
# from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from functools import wraps

import random
import string
from uuid import uuid4
from jose import jwt, JWTError
from datetime import datetime, timedelta

from src.models import (
    Token,
    TokenData,
    UserDB,
    UserLogIn,
    UserSingUp,
    UserEnum,
    UserFront
)

from services.application import Env
from src.DB import DB

# oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AutoService:

    @staticmethod
    def generate_code(num: int) -> str:
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=num))
        # return random.randint(10**(num-1), (10**num)-1)

    @staticmethod
    def get_hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    async def get_new_uuid(db):
        uuid4_id = str(uuid4())
        while await db.find_one({"_id": uuid4_id}):
            uuid4_id = str(uuid4())
        return uuid4_id

    @staticmethod
    def get_expire_delta(expires_delta: int = None):
        if expires_delta:
            expire = datetime.now() + timedelta(days=expires_delta)
        else:
            expire = datetime.now() + timedelta(days=Env.get_access_token_expire_days())
        print(expire)
        return expire

    @staticmethod
    async def create_user(user_data: UserSingUp) -> dict:
        print("\n\033[92mUser sing in:\033[0m   ", user_data, "\n")
        db = await DB.get_collection_db()
        existing_user = await db.find_one({"email": user_data.email})
        if existing_user:
            print("\n\033[90mUser exist:\033[0m   ", existing_user["email"])
            raise HTTPException(status_code=400, detail="User already exists")

        try:
            uuid = await AutoService.get_new_uuid(db)
            hash_pw = AutoService.get_hash_password(user_data.password)

            user_to_DB = UserDB.convert_base_user_to_userDB(
                user_data, user_id=uuid, hash_pw=hash_pw)
            verification_code = AutoService.create_verification_token(
                user_email=user_to_DB.email)

            await db.insert_one(user_to_DB.dict(by_alias=True))

            print("\n\033[92mUser sing in:\033[0m   ", user_to_DB, "\n")
            return {"Email": user_to_DB.email, "VerCode": verification_code}

        except Exception as error:
            print("\n\033[91m error: \033[0m", error)
            raise error

    @staticmethod
    async def set_verification_password(user_email: str, code: str) -> dict:
        try:
            hash_code = AutoService.get_hash_password(code)
            update_result = await DB.update(conditions={"email": user_email}, updates={"temp_hashed_password": hash_code, "change_password": False})
            if update_result["status"]:
                return {"message": "User temp password update"}
            else:
                raise HTTPException(
                    status_code=400, detail="No user found with this email")
        except Exception as e:
            raise e

    @staticmethod
    async def verify_temp_password(user_email: str, code: str):
        result = await AutoService.get_user_by_field(user_email)
        if result:
            if AutoService.verify_password(code, result["temp_hashed_password"]):
                try:
                    await DB.update(
                        conditions={"email": user_email},
                        updates={"change_password": True},
                        replace={"temp_hashed_password": ""},

                    )
                    return {"message": "Successfully match temporary password and user can update password"}
                except Exception as e:
                    raise e
            else:
                raise HTTPException(
                    status_code=400, detail="incorrect code")
        else:
            raise HTTPException(
                status_code=400, detail="No matching user")

    @staticmethod
    async def update_user_password(user_email: str, code: int) -> dict:
        try:
            hash_code = AutoService.get_hash_password(code)

            update_result = await DB.update(
                {"email": user_email, "change_password": True},
                {"hashed_password": hash_code},
                {"change_password": ""}
            )
            if update_result["status"]:
                return {"message": "User password update successfully"}
            else:
                raise HTTPException(
                    status_code=400, detail="No user found with this email")
        except Exception as e:
            raise e

    @staticmethod
    async def get_user_by_field(value: str, field: str = "email"):
        try:
            user = await DB.find({field: value})
            if not user:
                raise HTTPException(
                    status_code=404, detail="User not found")
            return user

        except Exception as error:
            print(f"\n\033[91m{str(error)}\033[0m")
            raise HTTPException(
                status_code=500, detail=f"An internal error occurred: {str(error)}")

    @staticmethod
    def verify_password(password: str, hash_password: str) -> bool:
        return pwd_context.verify(password, hash_password)

    @staticmethod
    async def authenticate(
        email: str,
        password: str = None,
        user_type: str = None,
    ) -> UserDB:
        user = await AutoService.get_user_by_field(value=email)

        if not user["active"]:
            print("User is not active")
            raise HTTPException(
                status_code=400, detail=f"User is not active")

        if user_type and user_type != user["user_type"]:
            print("User type incorrect")
            raise HTTPException(
                status_code=401, detail=f"User type incorrect")

        if password and not AutoService.verify_password(password=password, hash_password=user["hashed_password"]):
            print("Incorrect password")
            raise HTTPException(
                status_code=400, detail="Incorrect password")

        print("User authenticate")
        return UserDB(**user)

# >>> Tokens

    @staticmethod
    def create_verification_token(user_email: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode = {"email": user_email, "exp": expire}
        token = jwt.encode(to_encode, Env.get_verification_key(),
                           algorithm=Env.get_algorithm())
        return token

    @staticmethod
    def create_access_token(user_data: UserDB) -> str:
        access_key = Env.get_access_key()
        expire = AutoService.get_expire_delta()
        print("\033[92mUser:\033[0m", user_data)
        to_encode = {
            "user_id": user_data.id,
            "user_type": user_data.user_type,
            "hash_pw": user_data.hashed_password,
            "exp": expire
        }
        encoded_jwt = jwt.encode(to_encode, access_key,
                                 algorithm=Env.get_algorithm())
        return encoded_jwt

    @staticmethod
    def create_refresh_token(user_data: UserDB):
        access_key = Env.get_access_key()
        expire = AutoService.get_expire_delta(
            Env.get_refresh_token_expire_days())
        print("\033[92mUser:\033[0m", user_data)
        to_encode = {
            "user_id": user_data.id,
            "exp": expire
        }
        encoded_jwt = jwt.encode(to_encode, access_key,
                                 algorithm=Env.get_algorithm())
        return encoded_jwt

    @staticmethod
    def verify_refresh_token(refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, Env.get_refresh_key(), algorithms=[
                                 Env.get_algorithm()])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=401, detail="Invalid or expired refresh token")

    @staticmethod
    def verify_access_token(token: str, user_type: str = "user"):
        try:
            payload = jwt.decode(token, Env.get_access_key(user_type=user_type), algorithms=[
                                 Env.get_algorithm()])
            return payload
        except JWTError:
            return

    @staticmethod
    async def verify_account(verify_token: str):
        try:
            payload = jwt.decode(verify_token, Env.get_verification_key(), algorithms=[
                                 Env.get_algorithm()])
            update_result = await DB.update({"email": payload["email"]}, {"active": True})
            if update_result["status"]:
                return {"message": "User verified successfully"}
            else:
                raise HTTPException(
                    status_code=400, detail="No user found with this email or user already active")

        except JWTError:
            try:
                payload = jwt.decode(
                    verify_token,
                    Env.get_verification_key(),
                    algorithms=[Env.get_algorithm()],
                    options={"verify_exp": False}
                )
                raise HTTPException(
                    status_code=401, detail={"error": "Expired token", "email": payload["email"]})
            except Exception as e:
                raise HTTPException(
                    status_code=401, detail={"error": "false token"})


# >> decorators

def authenticate_user(func):
    @wraps(func)
    async def wrapper(request: Request, response: Response, *args, **kwargs):
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        if access_token:
            payload = AutoService.verify_access_token(access_token)
            if payload:
                return await func(request, response, *args, **kwargs)

        if refresh_token:
            payload = AutoService.verify_refresh_token(refresh_token)
            user = await AutoService.get_user_by_field(
                field="_id", value=payload["user_id"])
            new_access_token = AutoService.create_access_token(user_data=user)

            if new_access_token:
                response.set_cookie(
                    key="access_token", value=new_access_token, httponly=True, secure=True
                )
                return await func(request, response, *args, **kwargs)

        raise HTTPException(
            status_code=401, detail="Authentication required or tokens expired")

    return wrapper


def authenticate_login(func):
    @wraps(func)
    async def wrapper(request: Request, response: Response, *args, **kwargs):
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        if access_token:
            payload = AutoService.verify_access_token(
                token=access_token,)
            if payload:
                print("\033[92mDecode access token:\033[0m", payload)

                user = await AutoService.get_user_by_field(
                    field="_id", value=payload["user_id"])
                return UserFront(**user).dict(by_alias=False)

        if refresh_token:
            try:
                payload = AutoService.verify_refresh_token(refresh_token)
                if payload:
                    print("\033[92mDecode refresh token:\033[0m", payload)
                    user = AutoService.get_user_by_field(
                        field="_id", value=payload["user_id"])
                    new_access_token = AutoService.create_access_token(
                        user_data=user)
                    if new_access_token:
                        response.set_cookie(
                            key="access_token",
                            value=new_access_token,
                            httponly=True,
                            secure=True,
                            samesite="Lax"
                        )
                        return UserFront(**user).dict(by_alias=True)
            except Exception as e:
                print(f"Error in refresh token process: {e}")

        # >>> go to log-in
        print(">> go to log-in ")
        return await func(request, response, *args, **kwargs)

    return wrapper
