import json
from fastapi import Depends, HTTPException, Request, Response, status, APIRouter, Body, Path
from fastapi.security import OAuth2PasswordRequestForm

# >>> models


from src.models import (
    Token,
    Column,
    Row,
    BaseTable
)

# >>> services
from services.application import Env
from .user_service import UserService
import src.auto.auto_service as Auto


router = APIRouter(tags=["Users"])


@router.get("/get_by_id/{id}")
@Auto.authenticate_user
async def test(request: Request, response: Response, id: str) -> dict:
    print("user_id:", id)
    user = await UserService.get_user_by_field("_id", id)
    return {"user": user}


@router.post("/insert-new-table/{user_id}/{table_name}")
@Auto.authenticate_user
async def test(request: Request, response: Response, user_id: str, table_name: str, table_data: BaseTable):
    # the way to init json from db to object in pydantic
    # user_tables = UserTables(**table_db)
    # print(json.dumps(table_db, indent=2))
    # print(user_tables.model_dump_json(indent=2))
    print("user_id:", user_id)
    table_db = await UserService.add_table(user_id=user_id, table_name=table_name, table_data=table_data)
    return table_db


# rows API
@router.post("/add-row/t/{table_id}")
@Auto.authenticate_user
async def add_row(request: Request, response: Response, table_id: str, new_row: Row):
    print("user_id:", table_id)
    table_db = await UserService.add_row(table_id, new_row)
    return table_db


@router.post("/update-row/t/{table_id}/r/{row_id}/c/{column_id}/v/{value}")
@Auto.authenticate_user
async def add_row(
    request: Request,
    response: Response,
    table_id: str,
    row_id: str,
    column_id: str,
    value
):
    print("user_id:", table_id)
    table_db = await UserService.update_row(table_id, row_id, column_id, value)
    return table_db


@router.post("/delete-row/t/{table_id}/r/{row_id}")
@Auto.authenticate_user
async def add_row(request: Request, response: Response, table_id: str, row_id: str):
    print("user_id:", table_id)
    table_db = await UserService.delete_row(table_id, row_id)
    return table_db


# columns API
@router.post("/add-column/t/{table_id}")
@Auto.authenticate_user
async def add_row(request: Request, response: Response, table_id: str, column_data: Column):
    print("user_id:", table_id)
    table_db = await UserService.add_column(table_id, column_data)
    return table_db


@router.post("/delete-column/t/{table_id}")
@Auto.authenticate_user
async def add_row(request: Request, response: Response, table_id: str, column_id: str):
    print("user_id:", table_id)
    table_db = await UserService.delete_column(table_id, column_id)
    return table_db
