from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, WebSocket
from redis.asyncio import Redis
from starlette.websockets import WebSocketDisconnect

socket_router = APIRouter(
    prefix="/ws"
)


@socket_router.websocket("/lots/{lot_id}")
@inject
async def lot_ws(
    lot_id: UUID,
    ws: WebSocket,
    redis: FromDishka[Redis]
):
    await ws.accept()
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"lot:{lot_id}")

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                await ws.send_text(message["data"])
    except WebSocketDisconnect:
        pass
    finally:
        await pubsub.unsubscribe(f"lot:{lot_id}")
        await pubsub.aclose()
