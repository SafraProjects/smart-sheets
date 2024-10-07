from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

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

from ..application import Access
from ..DB import DBApplication

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")
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
        access_key = Access.get_access_key(user_type)
        return access_key

    @staticmethod
    def get_expire_delta(expires_delta: timedelta = None):
        if expires_delta:
            expire = datetime.utcnow() + timedelta(minutes=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=Access.get_access_token_expire())
        print(expire)
        return expire

    @staticmethod
    def verify_password(password: str, hash_password: str) -> bool:
        return pwd_context.verify(password, hash_password)

    @staticmethod
    async def authenticate(user_name, password):
        db = await DBApplication.get_users_db()
        user = await db.find_one({"name": user_name})
        if not user or user["active"] != False:
            return False
        if not AutoService.verify_password(password=password, hash_password=user["hashed_password"]):
            return False
        return user

    @staticmethod
    async def create_user(user_data: UserSingUp) -> UserDB:
        print(user_data)
        db = await DBApplication.get_users_db()

        existing_user = await db.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        try:
            uuid = await AutoService.get_new_uuid(db)
            hash_pw = AutoService.get_hash_password(user_data.password)

            verification_code = AutoService.create_verification_token()
            user_to_DB = UserDB.convert_base_user_to_userDB(
                user_data, user_id=uuid, hash_pw=hash_pw)

            await db.insert_one(user_to_DB.dict(by_alias=True))

            return {"Email": user_to_DB.email, "VerCode": verification_code}
        except Exception as error:
            print(error)
            raise error

    # @staticmethod
    # async def sing_in(user_data: UserLogIn) -> Token:
    #     user = await UserService.get_user_by_field("name", user_data.name)
    #     return AutoService.create_token(UserDB(**user))

# >>> Tokens

    @staticmethod
    def create_verification_token(user_email: str) -> str:
        expire = datetime.utcnow() + timedelta(hours=1)
        to_encode = {"email": user_email, "exp": expire}
        token = jwt.encode(to_encode, Access.get_access_key(),
                           algorithm=Access.get_algorithm())
        return token

    @staticmethod
    def create_token(user_data: UserDB, expires_delta: timedelta = None) -> Token:
        access_key = AutoService.get_user_secret_key(user_data.user_type)
        expire = AutoService.get_expire_delta(expires_delta)
        print(user_data)
        to_encode = {
            "user_id": user_data.id,
            "user_type": user_data.user_type,
            "hash_pw": user_data.hashed_password,
            "exp": expire
        }
        encoded_jwt = jwt.encode(to_encode, access_key,
                                 algorithm=Access.get_algorithm())
        return encoded_jwt

    @staticmethod
    def create_access_token(user_data: UserDB):
        access_key = AutoService.get_user_secret_key(user_data.user_type)
        expire = AutoService.get_expire_delta()
        print(user_data)
        to_encode = {
            "user_id": user_data.id,
            "user_type": user_data.user_type,
            "hash_pw": user_data.hashed_password,
            "exp": expire
        }
        encoded_jwt = jwt.encode(to_encode, access_key,
                                 algorithm=Access.get_algorithm())
        return encoded_jwt

    @staticmethod
    def create_refresh_token(user_data: UserDB):
        access_key = AutoService.get_user_secret_key(user_data.user_type)
        expire = AutoService.get_expire_delta()
        print(user_data)
        to_encode = {
            "user_id": user_data.id,
            "exp": expire
        }
        encoded_jwt = jwt.encode(to_encode, access_key,
                                 algorithm=Access.get_algorithm())
        return encoded_jwt

    @staticmethod
    def refresh_access_token(refresh_token: str):
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        try:
            payload = jwt.decode(refresh_token, Access.get_refresh_key(), algorithms=[
                                 Access.get_algorithm()])
            user_id = payload.get("user_id")
            if user_id is None:
                raise exception

            user_data = AutoService.authenticate(user_id)

            return AutoService.create_access_token(user_data=user_data)
        except JWTError:
            raise exception

    @staticmethod
    async def verify_token(token: str):
        try:
            payload = jwt.decode(token, Access.get_access_key(), algorithms=[
                                 Access.get_algorithm()])
            db = await DBApplication.get_users_db()
            update_result = await db.update_one({"email": payload["email"]}, {"$set": {"active": True}})
            if update_result.modified_count == 1:
                return {"message": "User verified successfully"}
            else:
                raise HTTPException(
                    status_code=400, detail="No user found with this email or user already active")

        except JWTError:
            raise HTTPException(
                status_code=401, detail="Invalid or expired token")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An error occurred: {str(e)}")
