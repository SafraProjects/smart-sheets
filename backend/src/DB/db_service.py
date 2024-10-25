from typing import Union, Optional, List, Tuple
from motor.motor_asyncio import AsyncIOMotorClient
from services.application.app_service import Env
import logging


class DB:
    _client = None
    _db_name = "smart_sheets"

    @staticmethod
    async def get_collection_db(db_name: str = "smart_sheets", collection_name: str = "users"):
        if DB._client is None:
            try:
                DB._client = AsyncIOMotorClient(Env.get_DB_port())
            except Exception as error:
                logging.error(f"Error connecting to DB: {error}")
                raise error
        return DB._client[db_name][collection_name]

    @staticmethod
    async def close_db():
        if DB._client:
            try:
                DB._client.close()
                DB._client = None
            except Exception as error:
                logging.error(
                    f"Failed to close the database connection: {error}")
                raise error

    @staticmethod
    async def find(
        conditions: Optional[dict] = None,
        fields: Optional[dict] = None,
        find_one: bool = False,
        sort_fields: Optional[List[Tuple[str, int]]] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        additional_options: Optional[dict] = None,
        db_name: str = None,
        collection_name: str = None,
    ) -> Union[dict, list]:

        db_name = db_name or DB._db_name
        collection_name = collection_name or "users"
        conditions = conditions or {}
        fields = fields or {}
        additional_options = additional_options or {}

        db = await DB.get_collection_db(db_name=db_name, collection_name=collection_name)

        if find_one:
            return await db.find_one(conditions, fields)

        cursor = db.find(conditions, fields)

        if additional_options.get("or_conditions"):
            cursor = cursor.or_(additional_options["or_conditions"])

        if sort_fields:
            cursor = cursor.sort(sort_fields)

        if limit:
            cursor = cursor.limit(limit)

        if skip:
            cursor = cursor.skip(skip)

        return await cursor.to_list(length=None)

    @staticmethod
    async def insert(
        documents: List[dict] = None,
        insert_one: bool = False,
        write_concern: Optional[dict] = None,
        db_name: str = None,
        collection_name: str = None,
    ) -> Union[dict, list]:

        db_name = db_name or DB._db_name
        collection_name = collection_name or "users"

        if documents is None:
            documents = [{}] if insert_one else []

        db = await DB.get_collection_db(db_name=db_name, collection_name=collection_name)

        try:
            if insert_one:
                result = await db.insert_one(documents[0])
                return {**documents[0], "_id": str(result.inserted_id)}

            results = await db.insert_many(documents)
            return [{"_id": str(inserted_id)} for inserted_id in results.inserted_ids]
        except Exception as e:
            logging.error(f"Insert failed: {e}")
            raise

    @staticmethod
    async def update(
        conditions: Optional[dict] = None,
        updates: Optional[dict] = None,
        replace: Optional[dict] = None,
        update_one: bool = False,
        upsert: bool = False,
        db_name: str = None,
        collection_name: str = None,
    ) -> Union[dict, list]:

        db_name = db_name or "smart_sheets"
        collection_name = collection_name or "users"

        if conditions is None:
            conditions = {}
        if updates is None:
            updates = {}

        if replace is None:
            replace = {}

        db = await DB.get_collection_db(db_name=db_name, collection_name=collection_name)

        try:
            if update_one:
                result = await db.update_one(conditions, {"$set": updates, "$unset": replace}, upsert=upsert)
                if result.modified_count > 0:
                    return {"message": "Document updated successfully", "status": True}
                return {"message": "No documents matched the query", "status": False}

            result = await db.update_many(conditions, {"$set": updates, "$unset": replace}, upsert=upsert)
            return {"modified_count": result.modified_count, "status": True}
        except Exception as e:
            logging.error(f"Update failed: {e}")
            raise

    @staticmethod
    async def delete(
        conditions: Optional[dict] = None,
        delete_one: bool = False,
        db_name: str = None,
        collection_name: str = None,
    ) -> dict:

        db_name = db_name or "smart_sheets"
        collection_name = collection_name or "users"

        if conditions is None:
            conditions = {}

        db = await DB.get_collection_db(db_name=db_name, collection_name=collection_name)

        try:
            if delete_one:
                result = await db.delete_one(conditions)
                if result.deleted_count > 0:
                    return {"message": "Document deleted successfully"}
                return {"message": "No document matched the query"}

            result = await db.delete_many(conditions)
            return {"message": f"{result.deleted_count} documents deleted successfully"}
        except Exception as e:
            logging.error(f"Delete failed: {e}")
            raise

    @staticmethod
    async def create_index(
        index_fields: List[Tuple[str, int]],
        db_name: str = "smart_sheets",
        collection_name: str = "users",
    ):
        if not isinstance(index_fields, list) or not all(isinstance(field, tuple) for field in index_fields):
            raise ValueError("index_fields must be a list of tuples")

        db = await DB.get_collection_db(db_name=db_name, collection_name=collection_name)

        try:
            result = await db.create_index(index_fields)
            return {"index_name": result, "message": "Index created successfully"}
        except Exception as e:
            logging.error(f"Failed to create index: {e}")
            raise


# יש הרבה שינוים אבל זה כרגע נראה בסדר,
