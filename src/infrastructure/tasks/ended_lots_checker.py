import json
from datetime import UTC, datetime

from dishka import AsyncContainer
from redis.asyncio import Redis
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.lot_entity import LotStatus
from infrastructure.db.models.lot_model import LotModel


async def make_check_ended_lots(ioc: AsyncContainer):
    """
    Background task that periodically checks for expired lots and notifies subscribers
    Queries the database for RUNNING lots whose ending_at has passed, marks them as ENDED,
    and publishes a 'lot_ended' event to the corresponding Redis pub/sub channel for each
    """

    redis = await ioc.get(Redis)

    async def check_ended_lots():
        async with ioc() as request_container:
            session = await request_container.get(AsyncSession)

            now = datetime.now(tz=UTC)
            stmt = (
                update(LotModel)
                .where(
                    LotModel.ending_at < now,
                    LotModel.lot_status == LotStatus.RUNNING
                )
                .values(lot_status=LotStatus.ENDED)
                .returning(LotModel.id)
            )
            result = await session.execute(stmt)
            ended_ids = result.scalars().all()
            await session.commit()

            for lot_id in ended_ids:
                msg = json.dumps({"type": "lot_ended", "lot_id": str(lot_id)})
                await redis.publish(f"lot:{lot_id}", msg)

    return check_ended_lots