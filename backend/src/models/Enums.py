from enum import Enum


class UserEnum(str, Enum):
    user = "user"
    admin = "admin"
    super_admin = "super_admin"
