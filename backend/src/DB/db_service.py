from motor.motor_asyncio import AsyncIOMotorClient
from services.application.app_service import Env


class DBApplication:
    _client = None

    @staticmethod
    async def get_users_db():
        if DBApplication._client is None:
            try:
                DBApplication._client = AsyncIOMotorClient(
                    Env.get_DB_port())
            except Exception as error:
                print(error)
                raise error
        return DBApplication._client.smart_sheets.users

    @staticmethod
    async def close_db():
        if DBApplication._client:
            try:
                DBApplication._client.close()
                DBApplication._client = None
            except Exception as error:
                print(f"Failed to close the database connection: {error}")
                raise error
