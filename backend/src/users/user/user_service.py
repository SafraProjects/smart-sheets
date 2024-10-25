from fastapi import (
    Depends,
    HTTPException,
    status,
)

# >>> models
from src.models import (
    UserDB,
    UserTables,
    Table,
    BaseTable
)

# >>> services
import src.DB.users_tables_service as DS
import src.DB.db_service as GDB


class UserService:

    @staticmethod
    async def get_user_by_field(filed: str, value: str) -> UserDB:
        credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
        user = await GDB.DB.find({filed: value}, find_one=True)
        if user is None:
            raise credential_exception
        return user

    @staticmethod
    async def add_table(user_id, table_name, table_data: BaseTable) -> UserTables:
        table_db = await DS.UsersTablesService.insert_table(
            user_id=user_id,
            table_name=table_name,
            columns=table_data.columns,
            rows=table_data.rows
        )
        return table_db

        # @staticmethod
        # async def sing_out():
        #     pass
