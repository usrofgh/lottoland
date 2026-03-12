from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.value_objects.price_vo import PriceVO


@dataclass(slots=True, kw_only=True)
class BidEntity(BaseEntity):
    bidder: str
    amount: PriceVO
    lot_id: UUID
