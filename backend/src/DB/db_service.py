from typing import Union, Optional, List, Tuple
from motor.motor_asyncio import AsyncIOMotorClient
from services.environment.env_service import Env
import logging


class DB:
    _client = None
    _db_name = None
    _collection_name: str = None
    _coll_users = "users"
    _coll_tables = "users_tables"
    _coll_metadata = "users_metadata"

    @staticmethod
    async def get_collection_db(db_name: str = None, collection_name: str = None):
        if DB._client is None:
            DB._db_name = db_name or DB._db_name or "smart_sheets"
            DB._collection_name = collection_name or DB._collection_name or "users"
            try:
                DB._client = AsyncIOMotorClient(Env.get_DB_port())
            except Exception as error:
                logging.error(f"Error connecting to DB: {error}")
                raise error

        return DB._client[DB._db_name][DB._collection_name]

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
        many: bool = False,
        sort_fields: Optional[List[Tuple[str, int]]] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        additional_options: Optional[dict] = None,
        db_name: str = None,
        collection_name: str = None,
    ) -> Union[dict, list]:

        DB._db_name = db_name or DB._db_name
        DB._collection_name = collection_name or DB._collection_name
        db = await DB.get_collection_db()

        conditions = conditions or {}
        fields = fields or {}
        additional_options = additional_options or {}

        if not many:
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
        # תמיכה במסמך יחיד או ברשימה
        documents: Union[dict, List[dict]] = None,
        many: bool = False,
        db_name: str = None,
        collection_name: str = None,
    ) -> Union[dict, list]:

        DB._db_name = db_name or DB._db_name
        DB._collection_name = collection_name or DB._collection_name
        db = await DB.get_collection_db()

        if documents is None:
            documents = [{}] if not many else []

        if not isinstance(documents, list):
            documents = [documents]

        try:
            if not many:
                result = await db.insert_one(documents[0])
                return {"_id": str(result.inserted_id), **documents[0]}

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
        array_updates: Optional[dict] = None,
        array_removals: Optional[dict] = None,
        increase: Optional[dict] = None,
        upsert: bool = False,
        many: bool = False,
        db_name: str = None,
        collection_name: str = None,
    ) -> Union[dict, list]:

        DB._db_name = db_name or DB._db_name
        DB._collection_name = collection_name or DB._collection_name
        db = await DB.get_collection_db()

        try:
            update_operations = {
                "$set": updates or {}, "$unset": replace or {}}

            if array_updates:
                update_operations["$push"] = array_updates

            if array_removals:
                update_operations["$pull"] = array_removals

            if increase:
                update_operations["$inc"] = increase

            if not many:
                result = await db.update_one(conditions or {}, update_operations, upsert=upsert)
            else:
                result = await db.update_many(conditions or {}, update_operations, upsert=upsert)

            if result.modified_count > 0:
                return {"message": "Document updated successfully", "status": True}
            return {"message": "No documents matched the query", "status": False}
        except Exception as e:
            logging.error(f"Update failed: {e}")
            raise

    @staticmethod
    async def delete(
        conditions: Optional[dict] = None,
        many: bool = False,
        db_name: str = None,
        collection_name: str = None,
    ) -> dict:

        DB._db_name = db_name or DB._db_name
        DB._collection_name = collection_name or DB._collection_name
        db = await DB.get_collection_db()

        if conditions is None:
            conditions = {}

        try:
            if not many:
                result = await db.delete_one(conditions)
            else:
                result = await db.delete_many(conditions)

            if result.deleted_count > 0:
                return {"message": f"{result.deleted_count} documents deleted successfully"}
            return {"message": "No document matched the query"}

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

        DB._db_name = db_name or DB._db_name
        DB._collection_name = collection_name or DB._collection_name
        db = await DB.get_collection_db()

        try:
            result = await db.create_index(index_fields)
            return {"index_name": result, "message": "Index created successfully"}
        except Exception as e:
            logging.error(f"Failed to create index: {e}")
            raise


# יש הרבה שינוים אבל זה כרגע נראה בסדר,
