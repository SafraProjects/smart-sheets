from typing import Set
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Set
from datetime import date, timedelta, datetime
from .Enums import TableTypeEnum


class Column(BaseModel):
    name: str
    type: str = "text"


class Row(BaseModel):
    data: Dict[str, str] = {}
    categories_includes: list[str] = []


class BaseTable(BaseModel):
    columns: Dict[str, Column]
    rows: Dict[str, Row]


class Table(BaseModel):
    id: str = Field(..., alias="_id")
    table_name: str
    type: str = "general"
    create_at: str = datetime.now().strftime("%Y-%m-%d")
    columns: Dict[str, Column] = Field(default_factory=dict)
    rows: Dict[str, Row] = Field(default_factory=dict)
    categories: Dict[str, int] = Field(default_factory=dict)

    def add_column(self, name: str, col_type: str = "text") -> None:
        new_col_id = "C-" + \
            str(int(max(self.columns.keys(), default="0").replace("C-", "")) + 1)
        self.columns[new_col_id] = Column(name=name, type=col_type)

    def add_row(self, row_data: Dict[str, str], categories: List[str] = []) -> None:
        new_row_id = "R-" + \
            str(int(max(self.rows.keys(), default="0").replace("R-", "")) + 1)
        self.rows[new_row_id] = Row(
            data=row_data, categories_includes=categories)
        for category in categories:
            self.categories[category] = self.categories.get(category, 0) + 1


class TableMetadata(BaseModel):
    table_name: str
    type: str
    create_at: str
    num_of_col: int
    num_of_rows: int
    num_of_categories: int

    @staticmethod
    def from_table(table: Table) -> "TableMetadata":
        return TableMetadata(
            table_name=table.table_name,
            type=table.type,
            create_at=table.create_at,
            num_of_col=len(table.columns),
            num_of_rows=len(table.rows),
            num_of_categories=len(table.categories.keys()),
        )


# # דוגמה לשימוש
# table = Table(table_id="user_123-1", table_name="Example Table")
# table.add_column(name="aaa")
# table.add_column(name="bbb")
# table.add_row(row_data={"aaa": "value1", "bbb": "value2"}, categories=["friends"])
# table.add_row(row_data={"aaa": "value3", "bbb": "value4"}, categories=["work"])

# print(table.json(indent=4))


# class Column(BaseModel):
#     col_id: str = None
#     name: str = None
#     type: str = "text"


# class Row(BaseModel):
#     row_id: str = None
#     data: Dict[str, str]
#     categories_includes: List[str] = []


# class TableMetadata(BaseModel):
#     table_id: str
#     table_name: str
#     type: str
#     create_at: str
#     num_of_col: int
#     num_of_rows: int
#     num_of_categories: int


# class Table(BaseModel):
#     table_id: str
#     table_name: str
#     type: str = TableTypeEnum.general.value
#     create_at: str = datetime.now().strftime("%Y-%m-%d")
#     columns: List[Column]
#     categories: List[Dict[str, int]] = []
#     rows: List[Row]


# class UserTables(BaseModel):
#     id: str = Field(..., alias="_id")
#     metadata: List[TableMetadata]
#     tables: List[Table]


# class BaseTable(BaseModel):
#     columns: List[Column]
#     rows: List[Row]
