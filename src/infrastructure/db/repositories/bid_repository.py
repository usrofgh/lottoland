from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.bid_entity import BidEntity
from domain.i_interfaces.i_bid_repo import IBidRepository
from domain.value_objects.price_vo import PriceVO
from infrastructure.db.models.bid_model import BidModel


class BidRepository(IBidRepository):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def save(self, bid_entity: BidEntity) -> None:
        model = self.from_entity(bid_entity)
        self._db.add(model)

    async def get_by_id(self, id: UUID) -> BidEntity | None:
        stmt = select(BidModel).where(BidModel.id == id)
        model = (await self._db.execute(stmt)).scalar_one_or_none()
        entity = self.to_entity(model) if model else None
        return entity

    async def get_bids_by_lot_id(self, lot_id: UUID) -> list[BidEntity]:
        stmt = select(BidModel).where(BidModel.lot_id == lot_id)
        models = (await self._db.execute(stmt)).scalars().all()
        entities = [self.to_entity(m) for m in models]
        return entities

    @staticmethod
    def to_entity(model: BidModel) -> BidEntity:
        entity = BidEntity(
            id=model.id,
            bidder=model.bidder,
            amount=PriceVO(model.amount),
            created_at=model.created_at,
            lot_id=model.lot_id
        )
        return entity

    @staticmethod
    def from_entity(entity: BidEntity) -> BidModel:
        model = BidModel(
            id=entity.id,
            bidder=entity.bidder,
            amount=entity.amount.value,
            created_at=entity.created_at,
            lot_id=entity.lot_id
        )
        return model
