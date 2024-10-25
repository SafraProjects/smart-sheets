import logging
from datetime import datetime

from typing import (
    Union,
    Optional,
    List,
    Tuple
)
# models
from src.models import (
    Row,
    Column,
    Table,
    TableMetadata,
    UserTables
)

# services
import src.DB.db_service as DS


class UsersTablesService:

    @staticmethod
    async def insert_table(user_id: str, table_name: str, columns: List[Column], rows: List[Row]) -> UserTables:

        # check user or user table if exists
        existing_user_tables = await DS.DB.find({"user_id": user_id}, find_one=True, collection_name="users_tables")
        new_table_id = None
        if existing_user_tables:
            existing_tables: List[Table] = existing_user_tables.get(
                "tables", [])
            if await UsersTablesService.is_table_exists(table_name, existing_tables):
                logging.warning(
                    f"Table '{table_name}' already exists for this user.")
            # get new id
            if existing_tables:
                last_table_id = existing_tables[-1].table_id
                new_table_id = f"t{int(last_table_id[1:]) + 1}"

        table_id = new_table_id or "t1"

        # המרה של העמודות והרשומות לאובייקטים
        new_columns = [Column(col_id=str(index), name=column.name, type=column.type)
                       for index, column in enumerate(columns, 1)]
        new_rows = [Row(row_id=str(index), data=row.data)
                    for index, row in enumerate(rows, 1)]
        table = Table(table_id=table_id, table_name=table_name,
                      columns=new_columns, rows=new_rows)
        table_metadata = TableMetadata(table_id=table.table_id, table_name=table.table_name, type=table.type,
                                       create_at=table.create_at, num_of_col=len(table.columns), num_of_rows=len(table.rows), num_of_categories=0)

        # אם קיימת רשומת משתמש, נוסיף את הטבלה החדשה לרשומה הקיימת
        if existing_user_tables:
            existing_user_tables['metadata'].append(table_metadata)
            existing_user_tables['tables'].append(table)
            return await DS.DB.update({"user_id": user_id}, {existing_user_tables}, update_one=True, collection_name="users_tables")
        else:
            # יצירת מבנה הנתונים עבור המשתמש
            # הכנסה של הנתונים כמילון
            user_tables = UserTables(id=user_id, metadata=[
                                     table_metadata.dict()], tables=[table.dict()])
            return await DS.DB.insert([user_tables.dict(by_alias=True)], insert_one=True, collection_name="users_tables")

    @staticmethod
    async def is_table_exists(table_name: str, tables: list[Table] = None) -> bool:
        table_exists = any(table.table_name ==
                           table_name for table in tables)
        return table_exists


{
    "user_id": "user_123",
    "metadata": [
        {
            "table_id": "t1",
            "table_name": "a",
            "type": "todo",
            "create_at": "07/10/1999",
            "num_of_col": 3,
            "num_of_rows": 2,
            "num_of_categories": 3
        }
    ],
    "tables": [
        {
            "table_id": "t1",
            "table_name": "a",
            "type": "todo",
            "create_at": "07/10/1999",
            "columns": [
                {
                    "col_id": "c1",
                    "name": "name",
                    "type": "text"
                },
                {
                    "col_id": "c2",
                    "name": "age",
                    "type": "number"
                },
                {
                    "col_id": "c3",
                    "name": "email",
                    "type": "email"
                }
            ],
            "categories": [
                {
                    "friends": 1
                },
                {
                    "family": 1
                },
                {
                    "work": 1
                }
            ],
            "rows": [
                {
                    "row_id": "r1",
                    "data": {
                        "name": "sss1",
                        "age": "25",
                        "email": "asd1@sdf.com"
                    },
                    "categories": [
                        "friends",
                        "work"
                    ]
                },
                {
                    "row_id": "r2",
                    "data": {
                        "name": "sss2",
                        "age": "30",
                        "email": "asd2@sdf.com"
                    },
                    "categories": [
                        "family"
                    ]
                }
            ]
        }
    ]
}


# # ייצוג עמודה אחת


# class Column(BaseModel):
#     name: str
#     type: str


# class Row(BaseModel):
#     data: Dict[str, str]


# class Table(BaseModel):
#     table_id: str
#     table_name: str
#     columns: List[Column]
#     rows: List[Row]
