from fastapi import (
    Depends,
    HTTPException,
    status,
)
from jose import jwt, JWTError
from uuid import uuid4

from ..DB import DBApplication
from ..auto import Token, TokenData
from ..application import Access

from .user_model import (
    BaseUser,
    UserSing,
    UserDB
)


class UserService:

    @staticmethod
    async def create_user(user_data: BaseUser) -> UserDB:
        print(user_data)
        db = await DBApplication.get_users_db()
        try:
            uuid4_id = str(uuid4())
            while await db.find_one({"_id": uuid4_id}):
                uuid4_id = str(uuid4())

            user = UserDB.convert_baseuser_to_user(user_data, uuid4_id)
            user_dict = user.dict(by_alias=True)

            await db.insert_one(user_dict)
            return user
        except Exception as error:
            print(error)
            raise error

    from ..auto.auto_service import AutoUser

    @staticmethod
    async def get_current_user(token: Token = Depends(AutoUser.get_token)):
        credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
        try:
            payload = jwt.decode(token, Access.get_access_key("super_admin"),
                                 algorithms=[Access.get_algorithm()])
            user_id: str = payload.get("user_id")
            if user_id is None:
                raise credential_exception

        except JWTError:
            raise credential_exception

        user = await UserService.get_user_by_field("_id", user_id)
        return user

    @staticmethod
    async def get_user_by_field(filed: str, user_id: str) -> UserDB:
        credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
        db = await DBApplication.get_users_db()
        user = await db.find_one({filed: user_id})
        if user is None:
            raise credential_exception
        return user

    @staticmethod
    async def authenticate(user_name, password):
        db = await DBApplication.get_users_db()
        user = await db.find_one({"name": user_name})
        if not user or user["active"] != False:
            return False
        from ..auto.auto_service import AutoUser
        if not AutoUser.verify_password(password=password, hash_password=user["hashed_password"]):
            return False
        return user

    @staticmethod
    async def sing_in(user_data: UserSing) -> Token:
        user = await UserService.get_user_by_field("name", user_data.name)
        from ..auto.auto_service import AutoUser
        return AutoUser.create_token(UserDB(**user))

    @staticmethod
    async def sing_out():
        pass
