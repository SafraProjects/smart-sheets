import json
from fastapi import Depends, HTTPException, Request, Response, status, APIRouter, Body, Path
from fastapi.security import OAuth2PasswordRequestForm

# >>> models
from src.models import (
    UserSingUp,
    UserLogIn,
    UserDB,
    Token,
    BaseTable,
    UserTables
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
async def test(request: Request, response: Response, user_id: str, table_name: str, table_data: BaseTable = Depends()) -> UserTables:
    # print("user_id:", user_id)
    # user_tables = UserTables(**table_db)
    # print(json.dumps(table_db, indent=2))
    # print(user_tables.model_dump_json(indent=2))
    table_db = await UserService.add_table(user_id=user_id, table_name=table_name, table_data=table_data)
    return table_db
