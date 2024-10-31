

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

# רשימת WebSocket למעקב אחרי כל החיבורים הפעילים
connected_clients: List[WebSocket] = []


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # מאשר את החיבור
    connected_clients.append(websocket)  # מוסיף את החיבור לרשימה

    try:
        # מאזין להודעות מהלקוח ושולח תשובות
        while True:
            data = await websocket.receive_text()  # מקבל טקסט מהלקוח
            print(f"Received message: {data}")

            # לדוגמה, שולח חזרה ללקוח אישור של ההודעה
            await websocket.send_text(f"Message received: {data}")

            # שליחת הודעות לכל החיבורים הפעילים
            for client in connected_clients:
                if client is not websocket:
                    await client.send_text(f"Broadcast: {data}")

    except WebSocketDisconnect:
        # מתבצע עם ניתוק לקוח
        connected_clients.remove(websocket)
        print("Client disconnected")
