from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.lot_entity import LotStatus
from infrastructure.db.base_model import BaseModel


class LotModel(BaseModel):
    __tablename__ = "lots"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    price: Mapped[int]
    min_price_step: Mapped[int]
    lot_status: Mapped[LotStatus]
    ending_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


    bids = relationship("BidModel", back_populates="lot")
