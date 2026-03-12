from dataclasses import dataclass
from datetime import datetime, UTC, timedelta

from domain.entities.lot_entity import LotEntity, LotStatus
from domain.i_interfaces.i_lot_repo import ILotRepository
from domain.value_objects.price_vo import PriceVO


@dataclass(slots=True, frozen=True)
class CreateLotCommand:
    lot_repository: ILotRepository

    async def __call__(
        self,
        price: int,
        min_price_step: int,
        duration_minutes: int
    ):
        ending_at = datetime.now(tz=UTC) + timedelta(minutes=duration_minutes)
        lot_entity = LotEntity(
            price=PriceVO(price),
            min_price_step=min_price_step,
            lot_status=LotStatus.RUNNING,
            ending_at=ending_at
        )
        await self.lot_repository.save(lot_entity)
