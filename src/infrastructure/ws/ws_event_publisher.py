import json
from uuid import UUID
from redis.asyncio import Redis

from domain.i_interfaces.i_event_publisher import IEventPublisher


class RedisEventPublisher(IEventPublisher):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def publish_bid_placed(self, lot_id: UUID, bidder: str, amount: int) -> None:
        msg = json.dumps({"type": "bid_placed", "lot_id": str(lot_id), "bidder": bidder, "amount": amount})
        await self._redis.publish(f"lot:{lot_id}", msg)
