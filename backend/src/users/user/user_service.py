import logging
from fastapi import (
    Depends,
    HTTPException,
    status,
)

# >>> models
from src.models import (
    UserDB,
    Table,
    BaseTable,
    TableMetadata,
    Column,
    Row,
)

# >>> services
import src.DB.db_service as DBS


class UserService:

    @staticmethod
    async def get_user_by_field(filed: str, value: str) -> UserDB:
        credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
        user = await DBS.DB.find({filed: value})
        if user is None:
            raise credential_exception
        return user

# >>> table functions

    @staticmethod
    async def add_table(user_id: str, table_name: str, table_data: BaseTable) -> dict:

        existing_user_metadata = await DBS.DB.find({"_id": user_id}, collection_name=DBS.DB._coll_metadata)
        print(existing_user_metadata)

        if existing_user_metadata:
            for table_meta in existing_user_metadata.get("tables_metadata", {}).values():
                if table_meta["table_name"] == table_name:
                    logging.warning(
                        f"Table '{table_name}' already exists for user '{user_id}'.")
                    return {"message": "Table with this name already exists", "status": False}

            last_index = max((int(table_id.split("-")[-1])
                             for table_id in existing_user_metadata.get("tables_metadata", {}).keys()), default=0) + 1
            new_table_id = f"{user_id}-{last_index}"

        else:
            new_table_id = f"{user_id}-1"

        table = Table(_id=new_table_id, table_name=table_name)

        for column in table_data.columns.values():
            table.add_column(name=column.name, col_type=column.type)

        for row in table_data.rows.values():
            table.add_row(row_data=row.data,
                          categories=row.categories_includes)

        table_metadata = TableMetadata.from_table(table)

        await DBS.DB.insert(table.dict(by_alias=True), collection_name=DBS.DB._coll_tables)

        if existing_user_metadata:
            metadata_update = {
                f"tables_metadata.{new_table_id}": table_metadata.dict(by_alias=True)}
            await DBS.DB.update({"_id": user_id}, metadata_update, collection_name=DBS.DB._coll_metadata)
        else:
            new_metadata = {
                "_id": user_id,
                "tables_metadata": {
                    new_table_id: table_metadata.dict(by_alias=True)
                }
            }
            await DBS.DB.insert(new_metadata, collection_name=DBS.DB._coll_metadata)

        return {"message": "Table and metadata inserted/updated successfully", "status": True}

# >>> row functions

    @staticmethod
    async def add_row(table_id: str, new_row: Row):

        new_row_index = f"R-{await UserService.get_last_row(table_id, num=True) + 1 or 1}"
        table_update = await DBS.DB.update(
            conditions={"_id": table_id},
            updates={f"rows.{new_row_index}": new_row.dict()},
            collection_name=DBS.DB._coll_tables
        )

        if not table_update["status"]:
            raise ValueError("Table update failed")

        metadata_update = await DBS.DB.update(
            conditions={"_id": table_id.rsplit('-', 1)[0]},
            increase={
                f"tables_metadata.{table_id}.num_of_rows": 1,
                # f"tables_metadata.{table_id}.num_of_categories": len(new_row_dict['categories_includes'])
            },
            collection_name=DBS.DB._coll_metadata
        )

        if not metadata_update["status"]:
            raise ValueError("Metadata update failed")

        return {"message": "Row added successfully", "status": True}

    @staticmethod
    async def delete_row(table_id: str, row_id: str):

        table_update = await DBS.DB.update(
            conditions={"_id": table_id},
            replace={f"rows.{row_id}": ""},
            collection_name=DBS.DB._coll_tables
        )

        if not table_update["status"]:
            raise ValueError("Table update failed")

        metadata_update = await DBS.DB.update(
            conditions={"_id": table_id.rsplit('-', 1)[0]},
            increase={f"tables_metadata.{table_id}.num_of_rows": -1},
            collection_name=DBS.DB._coll_metadata
        )

        if not metadata_update["status"]:
            raise ValueError("Metadata update failed")

        return {"message": "Row deleted successfully", "status": True}

    @staticmethod
    async def update_row(table_id: str, row_id: str, column_id: str, value):

        result = await DBS.DB.update(
            conditions={"_id": table_id},
            updates={f"rows.{row_id}.data.{column_id}": value},
            collection_name=DBS.DB._coll_tables
        )

        if not result["status"]:
            raise ValueError(
                f"Update of value '{value}' in row '{row_id}' failed")

        return result

    @staticmethod
    async def get_row(table_id: str, row_id: str) -> int:

        if not row_id.startswith("R-") or not row_id[2:].isdigit():
            return {"message": f"Invalid row index format: {row_id}", "status": False}

        result = await DBS.DB.find(
            conditions={"_id": table_id},
            fields={f"rows.{row_id}": 1},
            collection_name=DBS.DB._coll_tables
        )

        if not result:
            raise ValueError("Table not found")

        return result["rows"]

    @staticmethod
    async def get_last_row(table_id: str, num: bool = False) -> int:
        result = await DBS.DB.find(
            conditions={"_id": table_id},
            fields={"rows": 1},
            collection_name=DBS.DB._coll_tables
        )

        if not result:
            raise ValueError("Table not found")

        if not result.get("rows"):
            return 0

        last_index = sorted(result["rows"].keys())[-1]
        if not last_index.startswith("R-") or not last_index[2:].isdigit():
            raise ValueError(f"Invalid row index format: {last_index}")

        if num:
            return int(last_index[2:])
        return result["rows"][last_index]

# >>> columns functions

    @staticmethod
    async def add_column(table_id: str, new_column: Row):

        new_row_index = f"C-{await UserService.get_last_column(table_id, num=True) + 1 or 1}"
        table_update = await DBS.DB.update(
            conditions={"_id": table_id},
            updates={f"columns.{new_row_index}": new_column.dict()},
            collection_name=DBS.DB._coll_tables
        )

        if not table_update["status"]:
            raise ValueError("Table update failed")

        metadata_update = await DBS.DB.update(
            conditions={"_id": table_id.rsplit('-', 1)[0]},
            increase={
                f"tables_metadata.{table_id}.num_of_col": 1,
                # f"tables_metadata.{table_id}.num_of_categories": len(new_row_dict['categories_includes'])
            },
            collection_name=DBS.DB._coll_metadata
        )

        if not metadata_update["status"]:
            raise ValueError("Metadata update failed")

        return {"message": "Column added successfully", "status": True}

    @staticmethod
    async def delete_column(table_id: str, column_id: str):

        if not column_id.startswith("C-") or not column_id[2:].isdigit():
            return {"message": f"Invalid row index format: {column_id}", "status": False}

        is_column_deleted = await UserService.delete_column_from_rows(table_id, column_id)

        if not is_column_deleted["status"]:
            return is_column_deleted

        table_update = await DBS.DB.update(
            conditions={"_id": table_id},
            replace={f"columns.{column_id}": ""},
            collection_name=DBS.DB._coll_tables
        )

        if not table_update["status"]:
            return {"message": "Column deleted failed", "status": False}

        metadata_update = await DBS.DB.update(
            conditions={"_id": table_id.rsplit('-', 1)[0]},
            increase={f"tables_metadata.{table_id}.num_of_col": -1},
            collection_name=DBS.DB._coll_metadata
        )

        if not metadata_update["status"]:
            raise ValueError("Metadata update failed")

        return {"message": "Column deleted successfully", "status": True}

    @staticmethod
    async def get_last_column(table_id: str, num: bool = False) -> int:
        result = await DBS.DB.find(
            conditions={"_id": table_id},
            fields={"columns": 1},
            collection_name=DBS.DB._coll_tables
        )

        if not result:
            raise ValueError("Table not found")

        if not result.get("columns"):
            return 0

        last_index = sorted(result["columns"].keys())[-1]
        if not last_index.startswith("C-") or not last_index[2:].isdigit():
            raise ValueError(f"Invalid row index format: {last_index}")

        if num:
            return int(last_index[2:])
        return result["columns"][last_index]

    @staticmethod
    async def delete_column_from_rows(table_id: str, column_id: str):

        document = await DBS.DB.find({"_id": table_id}, {"rows": 1}, collection_name=DBS.DB._coll_tables)
        if not document:
            return {"message": "Table not found", "status": False}

        updates = {
            f"rows.{row_id}.data.{column_id}": "" for row_id in document["rows"].keys()}

        result = await DBS.DB.update(
            conditions={"_id": table_id},
            replace=updates,
            collection_name=DBS.DB._coll_tables
        )

        if result["status"]:
            return {"message": "Column deleted successfully from the rows", "status": True}
        return {"message": "Failed to delete column from the rows", "status": False}
