from fastapi import (
    Depends,
    HTTPException,
    status,
)

# >>> models
from src.models import (
    UserDB,
)

# >>> services
from src.DB import DBApplication


class UserService:

    @staticmethod
    async def get_user_by_field(filed: str, value: str) -> UserDB:
        credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
        db = await DBApplication.get_users_db()
        user = await db.find_one({filed: value})
        if user is None:
            raise credential_exception
        return user

    # @staticmethod
    # async def sing_out():
    #     pass
