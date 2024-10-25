from enum import Enum


class UserEnum(str, Enum):
    user = "user"
    admin = "admin"
    super_admin = "super_admin"


class TableTypeEnum(str, Enum):
    general = "general"
    context = "context"
    todo = "todo"
