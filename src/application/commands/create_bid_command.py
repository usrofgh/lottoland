from dataclasses import dataclass
from uuid import UUID

from bootstrap.settings import Settings
from domain.entities.bid_entity import BidEntity
from domain.errors import ErrorCodes, DomainError
from domain.i_interfaces.i_bid_repo import IBidRepository
from domain.i_interfaces.i_event_publisher import IEventPublisher
from domain.i_interfaces.i_lot_repo import ILotRepository
from domain.value_objects.price_vo import PriceVO


@dataclass(slots=True, frozen=True)
class CreateBidCommand:
    bid_repository: IBidRepository
    lot_repository: ILotRepository
    event_publisher: IEventPublisher
    settings: Settings

    async def __call__(
        self,
        lot_id: UUID,
        bidder: str,
        amount: int
    ):
        found_lot = await self.lot_repository.get_by_id(lot_id)
        if not found_lot:
            raise DomainError(ErrorCodes.LOT_NOT_FOUND)

        new_bid = BidEntity(
            bidder=bidder,
            amount=PriceVO(amount),
            lot_id=lot_id
        )

        db_bids = await self.bid_repository.get_bids_by_lot_id(lot_id)
        found_lot.validate_new_bid(new_bid, db_bids)
        await self.bid_repository.save(new_bid)

        await self.event_publisher.publish_bid_placed(lot_id, bidder, amount)
