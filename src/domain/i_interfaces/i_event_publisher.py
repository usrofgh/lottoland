from abc import ABC, abstractmethod
from uuid import UUID


class IEventPublisher(ABC):
    @abstractmethod
    async def publish_bid_placed(
        self,
        lot_id: UUID,
        bidder: str,
        amount: int
    ):
        ...
