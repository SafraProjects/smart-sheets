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

    @staticmethod
    async def add_row(user_id: str, table_index: int, new_row: Row):
        table_id = f"{user_id}-{table_index}"

        # הכנת הערכים החדשים
        new_row_dict = new_row.dict()
        new_row_dict['categories_includes'] = new_row_dict.get(
            "categories_includes", [])

        # שליפת הטבלה
        table_doc = await DBS.DB.find({"_id": table_id}, collection_name=DBS.DB._coll_users)

        if not table_doc:
            raise ValueError("Table not found")

        # קביעת מפתח השורה החדשה
        current_rows = table_doc.get('rows', {})
        last_row_key = int(
            max(current_rows.keys(), default="0").replace("R-", "")) + 1
        new_row_index = "R-" + str(last_row_key)

        # עדכון הטבלה
        updates = {
            f"rows.{new_row_index}": new_row_dict,
        }

        table_update = await DBS.DB.update(
            conditions={"_id": table_id},
            updates=updates,
            collection_name=DBS.DB._coll_tables
        )

        if not table_update.get("status", False):
            raise ValueError("Table update failed")

        # עדכון המטאדאטה
        metadata_update = await DBS.DB.update(
            conditions={"_id": user_id},
            increase={
                f"tables_metadata.{table_id}.num_of_rows": 1,
                # f"tables_metadata.{table_id}.num_of_categories": len(new_row_dict['categories_includes'])
            },
            collection_name=DBS.DB._coll_metadata
        )

        # בדוק אם העדכון הצליח
        if not metadata_update.get("status", False):
            raise ValueError("Metadata update failed")

        return {"message": "Row added successfully", "status": True}

        # @staticmethod
        # async def sing_out():
        #     pass
