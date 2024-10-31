from fastapi import WebSocket
from typing import Dict, Optional
import asyncio


lock = asyncio.Lock()


class ConnectionManager:
    def __init__(self):
        # {room_id: {user_id: WebSocket}}
        self.rooms: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str, room_id: str):
        async with lock:
            # וידוא שהחדר קיים, אחרת ניצור אותו
            if room_id not in self.rooms:
                self.rooms[room_id] = {}

            # אם כבר יש חיבור פעיל לאותו user_id, נסגור אותו
            if user_id in self.rooms[room_id]:
                await self.rooms[room_id][user_id].close()

            # קבלה של החיבור החדש
            await websocket.accept()
            self.rooms[room_id][user_id] = websocket

    async def disconnect(self, user_id: str, room_id: str):
        async with lock:
            if room_id in self.rooms and user_id in self.rooms[room_id]:
                del self.rooms[room_id][user_id]

            # מחיקת חדרים ריקים
            if not self.rooms[room_id]:
                del self.rooms[room_id]

    async def send_personal_message(self, message: str, user_id: str, room_id: str):
        # שליחת הודעה פרטית למשתמש בחדר מסוים
        if room_id in self.rooms and user_id in self.rooms[room_id]:
            try:
                await self.rooms[room_id][user_id].send_text(message)
            except Exception:
                await self.disconnect(user_id, room_id)

    async def broadcast(self, message: str, room_id: str, exclude_user: Optional[str] = None):
        # שידור הודעה לכל משתמשי החדר פרט לאחד שהוגדר (לא חובה)
        async with lock:
            if room_id in self.rooms:
                for user_id, connection in self.rooms[room_id].items():
                    if user_id != exclude_user:
                        try:
                            await connection.send_text(message)
                        except Exception:
                            await self.disconnect(user_id, room_id)


# פונקציה לקבלת מנהל החיבורים
def get_websocket_manager():
    return ConnectionManager()


# router = APIRouter()

# # רשימת WebSocket למעקב אחרי כל החיבורים הפעילים
# connected_clients: Dict[str, WebSocket] = {}


# @router.websocket("/{user_id}")
# async def websocket_endpoint(websocket: WebSocket, user_id: str):
#     await websocket.accept()  # מאשר את החיבור
#     connected_clients[user_id] = websocket  # מוסיף את החיבור לרשימה

#     try:
#         # מאזין להודעות מהלקוח ושולח תשובות
#         while True:
#             data = await websocket.receive_text()  # מקבל טקסט מהלקוח
#             print(f"Received message: {data}")

#             # לדוגמה, שולח חזרה ללקוח אישור של ההודעה
#             await websocket.send_text(f"Message received: {data}")

#             # שליחת הודעות לכל החיבורים הפעילים
#             for client in connected_clients:
#                 if connected_clients[client] is not websocket:
#                     await connected_clients[client].send_text(f"Broadcast: {data}")

#     except WebSocketDisconnect:
#         # מתבצע עם ניתוק לקוח
#         del connected_clients[client]
#         print("Client disconnected")
