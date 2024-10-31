from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .websoket_service import get_websocket_manager

router = APIRouter()
manager = get_websocket_manager()


@router.websocket("/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, room_id: str):
    manager = get_websocket_manager()
    await manager.connect(websocket, user_id, room_id)

    try:
        while True:
            data = await websocket.receive_text()
            print(
                f"Received message from user {user_id} in room {room_id}: {data}")

            # דוגמה לעיבוד הודעות לפי סוג
            if data == "broadcast":
                await manager.broadcast(f"Broadcast message from {user_id}", room_id, exclude_user=user_id)
            elif data.startswith("private:"):
                target_user_id = data.split(":")[1]
                await manager.send_personal_message(f"Private message from {user_id}", target_user_id, room_id)
            else:
                await websocket.send_text(f"Echo: {data}")

    except WebSocketDisconnect:
        await manager.disconnect(user_id, room_id)
        print(f"User {user_id} disconnected from room {room_id}")
