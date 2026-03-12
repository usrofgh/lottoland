from dataclasses import dataclass

import datetime
from enum import StrEnum

from domain.entities.base import BaseEntity
from domain.entities.bid_entity import BidEntity
from domain.errors import DomainError, ErrorCodes
from domain.value_objects.price_vo import PriceVO


class LotStatus(StrEnum):
    RUNNING = "RUNNING"
    ENDED = "ENDED"


@dataclass(slots=True, kw_only=True)
class LotEntity(BaseEntity):
    price: PriceVO
    min_price_step: int
    lot_status: LotStatus
    ending_at: datetime.datetime

    def is_lot_ended(self) -> bool:
        now = datetime.datetime.now(tz=datetime.UTC)
        is_ended = now >= self.ending_at
        return is_ended

    def validate_new_bid(
        self,
        new_bid: BidEntity,
        bids: list[BidEntity],
    ) -> None:
        if self.is_lot_ended():
            raise DomainError(ErrorCodes.LOT_IS_ENDED)

        max_price = 0
        for db_bid in bids:
            if new_bid.amount <= db_bid.amount:
                raise DomainError(ErrorCodes.BID_NOT_MORE_THAN_EXISTENCE)
            if max_price < db_bid.amount.value:
                max_price = db_bid.amount.value

        if abs(new_bid.amount.value - max_price) < self.min_price_step:
            raise DomainError(ErrorCodes.TOO_SMALL_STEP)
