import os
from dotenv import load_dotenv

load_dotenv()


class Access():
    @staticmethod
    def get_access_key(user_type: str = "user") -> str:
        user_access_key = user_type + "_access_key"
        return os.getenv(user_access_key)

    @staticmethod
    def get_refresh_key() -> str:
        return os.getenv("refresh_key")

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
