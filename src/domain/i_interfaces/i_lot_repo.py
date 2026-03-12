from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.lot_entity import LotEntity


class ILotRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> LotEntity:
        ...

    @abstractmethod
    async def save(self, lot_entity: LotEntity) -> None:
        ...

    @abstractmethod
    async def update(self, changed_lot_entity: LotEntity):
        ...
