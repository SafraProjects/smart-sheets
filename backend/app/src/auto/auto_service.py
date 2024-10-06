from fastapi import Depends, status, HTTPException

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from jose import jwt, JWTError
from datetime import datetime, timedelta

from ..enums import UserEnum
from .auto_model import (
    Token,
    TokenData,
    UserDB,
    UserSing
)
from ..application import Access
from ..DB import DBApplication

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AutoUser:

    @staticmethod
    def get_hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hash_password: str) -> bool:
        return pwd_context.verify(password, hash_password)

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
    def create_token(user_data: UserDB, expires_delta: timedelta = None) -> Token:
        access_key = AutoUser.get_user_secret_key(user_data["user_type"])
        expire = AutoUser.get_expire_delta(expires_delta)
        to_encode = {
            "user_id": user_data["_id"],
            "user_type": user_data["user_type"],
            "exp": expire
        }
        encoded_jwt = jwt.encode(to_encode, access_key,
                                 algorithm=Access.get_algorithm())
        return encoded_jwt

    @staticmethod
    def get_token(token: Token = Depends(oauth2_schema)) -> Token:
        return token
