from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.base_model import BaseModel


class BidModel(BaseModel):
    __tablename__ = "bids"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    bidder: Mapped[str]
    amount: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    lot_id: Mapped[UUID] = mapped_column(ForeignKey("lots.id"))
    lot = relationship("LotModel", back_populates="bids")
