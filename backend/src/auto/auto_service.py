from fastapi import Depends, status, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from functools import wraps


from jose import jwt, JWTError
from uuid import uuid4
from datetime import datetime, timedelta

from src.models import (
    Token,
    TokenData,
    UserDB,
    UserLogIn,
    UserSingUp,
    UserEnum
)

from ..application import Env
from ..DB import DBApplication

# oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AutoService:

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
    def get_user_secret_key(user_type: UserEnum) -> str:
        access_key = Env.get_access_key(user_type)
        return access_key

    @staticmethod
    def get_expire_delta(expires_delta: int = None):
        if expires_delta:
            expire = datetime.now() + timedelta(days=expires_delta)
        else:
            expire = datetime.now() + timedelta(days=Env.get_access_token_expire_days())
        print(expire)
        return expire

    @staticmethod
    def verify_password(password: str, hash_password: str) -> bool:
        return pwd_context.verify(password, hash_password)

    @staticmethod
    async def get_user_by_field(value: str, field: str = "email", db=None):
        try:
            if not db:
                db = await DBApplication.get_users_db()
            user = await db.find_one({field: value})
            if not user:
                raise HTTPException(
                    status_code=404, detail="User not found")
            return user

        except Exception as error:
            print(f"\n\033[91m{str(error)}\033[0m")
            raise HTTPException(
                status_code=500, detail=f"An internal error occurred: {str(error)}")

    @staticmethod
    async def authenticate(
        email: str,
        password: str = None,
        user_type: str = None,
    ) -> UserDB:
        user = await AutoService.get_user_by_field(value=email)

        if not user["active"]:
            print("a")
            raise HTTPException(
                status_code=400, detail=f"User is not active")

        if user_type and user_type != user["user_type"]:
            print("b")
            raise HTTPException(
                status_code=401, detail=f"User type incorrect")

        if password and not AutoService.verify_password(password=password, hash_password=user["hashed_password"]):
            print("c")
            raise HTTPException(
                status_code=400, detail="Incorrect password")

        print("d")
        return UserDB(**user)

    @staticmethod
    async def create_user(user_data: UserSingUp) -> dict:
        print("\n\033[92mUser sing in:\033[0m   ", user_data, "\n")
        db = await DBApplication.get_users_db()
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


# >>> Tokens

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
            db = await DBApplication.get_users_db()
            update_result = await db.update_one({"email": payload["email"]}, {"$set": {"active": True}})
            if update_result.modified_count == 1:
                return {"message": "User verified successfully"}
            else:
                raise HTTPException(
                    status_code=400, detail="No user found with this email or user already active")

        except JWTError:
            payload = jwt.decode(
                verify_token,
                Env.get_verification_key(),
                algorithms=[Env.get_algorithm()],
                options={"verify_exp": False}
            )
            raise HTTPException(
                status_code=401, detail={"error": "Invalid or expired token", "email": payload["email"]})

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An error occurred: {str(e)}")

    @staticmethod
    def create_verification_token(user_email: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode = {"email": user_email, "exp": expire}
        token = jwt.encode(to_encode, Env.get_verification_key(),
                           algorithm=Env.get_algorithm())
        return token

    # @staticmethod
    # def create_token(user_data: UserDB) -> Token:
    #     access_key = AutoService.get_user_secret_key(user_data.user_type)
    #     expire = AutoService.get_expire_delta()
    #     print("\033[92mUser:\033[0m", user_data)
    #     to_encode = {
    #         "user_id": user_data.id,
    #         "user_type": user_data.user_type,
    #         "hash_pw": user_data.hashed_password,
    #         "exp": expire
    #     }
    #     encoded_jwt = jwt.encode(to_encode, access_key,
    #                              algorithm=Env.get_algorithm())
    #     return encoded_jwt

    @staticmethod
    def create_access_token(user_data: UserDB) -> str:
        access_key = AutoService.get_user_secret_key()
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
        access_key = AutoService.get_user_secret_key()
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
                print(payload)
                user = await AutoService.get_user_by_field(
                    field="_id", value=payload["user_id"])
                return user

        if refresh_token:
            try:
                payload = AutoService.verify_refresh_token(refresh_token)
                if payload:
                    print(payload)
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
                        return {"user_data": user}
            except Exception as e:
                print(f"Error in refresh token process: {e}")

        # >>> go to log-in
        print(">>")
        return await func(request, response, *args, **kwargs)

    return wrapper
