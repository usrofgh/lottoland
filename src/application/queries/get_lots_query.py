from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.lot_entity import LotStatus
from infrastructure.db.models.lot_model import LotModel


class GetActiveLotsQuery:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def __call__(self) -> list[dict]:
        now = datetime.now(tz=UTC)
        stmt = select(LotModel).where(
            LotModel.lot_status == LotStatus.RUNNING,
            LotModel.ending_at > now
        )
        result = await self._db.execute(stmt)
        records = [row.__dict__ for row in result.scalars()]

        lots = []
        for record in records:
            del record["_sa_instance_state"]
            lots.append(record)
        return lots
