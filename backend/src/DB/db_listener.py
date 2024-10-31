import asyncio
from .db_service import DB


class DBListener:
    _listener_task = None
    _is_listening = False

    @staticmethod
    async def listen_to_changes(collection_name: str, field_name: str):
        db = await DB.get_collection_db(collection_name=collection_name)

        # פתח את ה-Change Stream
        async with db.watch([{"$match": {"operationType": "update"}}]) as stream:
            async for change in stream:
                updated_fields = change["updateDescription"]["updatedFields"]
                if field_name in updated_fields:
                    new_value = updated_fields[field_name]
                    print(f"Field '{field_name}' updated:", new_value)
                    # כאן תוכל להוסיף לוגיקה נוספת כמו העברת הערך לקולקציה אחרת

    @staticmethod
    async def start_listener(collection_name: str, field_name: str):
        if not DBListener._is_listening:
            DBListener._is_listening = True
            DBListener._listener_task = asyncio.create_task(
                DBListener.listen_to_changes(collection_name, field_name))
            print("Listener started.")

    @staticmethod
    async def stop_listener():
        if DBListener._is_listening:
            DBListener._is_listening = False
            if DBListener._listener_task:
                DBListener._listener_task.cancel()
                try:
                    await DBListener._listener_task
                except asyncio.CancelledError:
                    pass
            print("Listener stopped.")
