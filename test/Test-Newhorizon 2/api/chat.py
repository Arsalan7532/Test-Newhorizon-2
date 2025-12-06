from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from redis_managers.redis_manager import RedisManager
from services import crud
from database import get_db
import asyncio

router = APIRouter()
redis_manager = RedisManager()
connected_clients = {}  # key = user_id, value = WebSocket

# =========================
# WebSocket برای چت
# =========================
async def redis_listener():
    try:
        pubsub = await redis_manager.get_pubsub()  # async
        if pubsub:
            async for message in pubsub.listen():
                if message['type'] == 'message':
                    data = message['data'].decode()
                    # ارسال به کاربران آنلاین
                    for ws in connected_clients.values():
                        try:
                            await ws.send_text(data)
                        except Exception as e:
                            print(f"Error sending message to client: {e}")
        else:
            print("Failed to create Redis pubsub")
    except Exception as e:
        print(f"Redis listener error: {e}")


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(ws: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await ws.accept()
    connected_clients[user_id] = ws
    try:
        while True:
            data = await ws.receive_text()  # فرمت: receiver_id|content
            receiver_id_str, content = data.split("|", 1)
            receiver_id = int(receiver_id_str)

            # ذخیره پیام در دیتابیس
            crud.send_message(db, sender_id=user_id, receiver_id=receiver_id, content=content)

            # انتشار پیام به Redis برای broadcast
            await redis_manager.publish("chat", f"{user_id}|{receiver_id}|{content}")

    except WebSocketDisconnect:
        connected_clients.pop(user_id)
