import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Env():
    @staticmethod
    def get_access_key(user_type: str = "user") -> Optional[str]:
        user_access_key = user_type + "_access_key"
        return os.getenv(user_access_key)

    @staticmethod
    def get_refresh_key() -> Optional[str]:
        return os.getenv("refresh_key")

    @staticmethod
    def get_verification_key() -> Optional[str]:
        return os.getenv("verification_key")

    @staticmethod
    def get_algorithm() -> Optional[str]:
        return os.getenv("algorithm")

    @staticmethod
    def get_access_token_expire_days() -> int:
        value = os.getenv("token_access_expire_days")
        return int(value or 1)

    @staticmethod
    def get_refresh_token_expire_days() -> int:
        value = os.getenv("refresh_access_expire_days")
        return int(value or 1)

    @staticmethod
    def get_DB_port() -> Optional[str]:
        return os.getenv("mongo_port")

    @staticmethod
    def get_backend_port() -> Optional[str]:
        return os.getenv("backend_port")

    @staticmethod
    def get_frontend_port() -> Optional[str]:
        return os.getenv("frontend_port")

    @staticmethod
    def get_app_gmail_password() -> Optional[str]:
        return os.getenv("app_gmail")
