from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict
from datetime import date, timedelta, datetime
from .Enums import TableTypeEnum


class Column(BaseModel):
    col_id: str = None
    name: str = None
    type: str = "text"


class Row(BaseModel):
    row_id: str = None
    data: Dict[str, str]
    categories: List[str] = []


class TableMetadata(BaseModel):
    table_id: str
    table_name: str
    type: str
    create_at: str = datetime.now().isoformat()
    num_of_col: int
    num_of_rows: int
    num_of_categories: int


class Table(BaseModel):
    table_id: str
    table_name: str
    type: str = TableTypeEnum.general.value
    create_at: str = datetime.now().isoformat()
    columns: List[Column]
    categories: List[Dict[str, int]] = []
    rows: List[Row]


class UserTables(BaseModel):
    id: str = Field(..., alias="_id")
    metadata: List[TableMetadata]
    tables: List[Table]


class BaseTable(BaseModel):
    columns: List[Column]
    rows: List[Row]
