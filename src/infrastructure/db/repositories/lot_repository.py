from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.lot_entity import LotEntity
from domain.i_interfaces.i_lot_repo import ILotRepository
from domain.value_objects.price_vo import PriceVO
from infrastructure.db.models.lot_model import LotModel


class LotRepository(ILotRepository):
    async def update(self, changed_lot_entity: LotEntity):
        model = self.from_entity(changed_lot_entity)
        await self._db.merge(model)

    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_by_id(self, id: UUID) -> LotEntity | None:
        stmt = select(LotModel).where(LotModel.id == id)
        model = (await self._db.execute(stmt)).scalar_one_or_none()
        entity = self.to_entity(model) if model else None
        return entity

    async def save(self, lot_entity: LotEntity) -> None:
        model = self.from_entity(lot_entity)
        self._db.add(model)

    @staticmethod
    def to_entity(model: LotModel) -> LotEntity:
        return LotEntity(
            id=model.id,
            price=PriceVO(model.price),
            min_price_step=model.min_price_step,
            lot_status=model.lot_status,
            ending_at=model.ending_at,
            created_at=model.created_at,
        )

    @staticmethod
    def from_entity(entity: LotEntity) -> LotModel:
        return LotModel(
            id=entity.id,
            price=entity.price.value,
            min_price_step=entity.min_price_step,
            lot_status=entity.lot_status,
            ending_at=entity.ending_at,
            created_at=entity.created_at
        )
