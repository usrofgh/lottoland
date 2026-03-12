from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.errors import DomainError, ErrorCodes
from domain.i_interfaces.i_lot_repo import ILotRepository
from infrastructure.db.models.bid_model import BidModel


class GetBidsQuery:
    def __init__(
        self,
        db: AsyncSession,
        lot_repository: ILotRepository
    ):
        self._db = db
        self._lot_repository = lot_repository

    async def __call__(self, lot_id: UUID) -> list[dict]:
        db_lot = await self._lot_repository.get_by_id(lot_id)
        if not db_lot:
            raise DomainError(ErrorCodes.LOT_NOT_FOUND)

        stmt = select(BidModel).where(BidModel.lot_id == lot_id)
        result = await self._db.execute(stmt)
        records = [row.__dict__ for row in result.scalars()]

        lots = []
        for record in records:
            del record["_sa_instance_state"]
            lots.append(record)
        return lots
