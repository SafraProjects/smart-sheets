import os
from dotenv import load_dotenv

load_dotenv()


class Access():
    @staticmethod
    def get_access_key(user_type: str = "user") -> str:
        user_access = "access_key" if user_type == "user" else "admin_access_key" if user_type == "admin" else "super_admin_access_key" if user_type == "super_admin" else "access_key"
        return os.getenv(user_access)

    @staticmethod
    def get_algorithm() -> str:
        return os.getenv("algorithm")

    @staticmethod
    def get_access_token_expire() -> int:
        value = os.getenv("access_token_expire")
        if value is None:
            return 3
        return int(value)

    @staticmethod
    def get_DB_port() -> str:
        return os.getenv("mongo_port")
