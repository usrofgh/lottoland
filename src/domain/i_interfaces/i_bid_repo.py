from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.bid_entity import BidEntity


class IBidRepository(ABC):
    @abstractmethod
    async def save(self, bid_entity: BidEntity) -> None:
        ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> None:
        ...

    @abstractmethod
    async def get_bids_by_lot_id(self, lot_id: UUID) -> list[BidEntity]:
        ...