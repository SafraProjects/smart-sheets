
from src.auto.auto_service import AutoService
from src.users.user.user_service import UserService


async def get_user_service() -> UserService:
    return UserService()


async def get_auto_user() -> AutoService:
    return AutoService()
