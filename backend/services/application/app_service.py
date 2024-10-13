import os
from dotenv import load_dotenv

load_dotenv()


class Env():
    @staticmethod
    def get_access_key(user_type: str = "user") -> str:
        user_access_key = user_type + "_access_key"
        return os.getenv(user_access_key)

    @staticmethod
    def get_refresh_key() -> str:
        return os.getenv("refresh_key")

    @staticmethod
    def get_verification_key() -> str:
        return os.getenv("verification_key")

    @staticmethod
    def get_algorithm() -> str:
        return os.getenv("algorithm")

    @staticmethod
    def get_access_token_expire_days() -> int:
        value = os.getenv("token_access_expire_days")
        return int(value)

    @staticmethod
    def get_refresh_token_expire_days() -> int:
        value = os.getenv("refresh_access_expire_days")
        return int(value)

    @staticmethod
    def get_DB_port() -> str:
        return os.getenv("mongo_port")

    @staticmethod
    def get_backend_port() -> str:
        return os.getenv("backend_port")

    @staticmethod
    def get_frontend_port() -> str:
        return os.getenv("frontend_port")

    @staticmethod
    def get_app_gmail_password() -> str:
        return os.getenv("app_gmail")
