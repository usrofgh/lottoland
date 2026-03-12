from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from domain.entities.lot_entity import LotStatus


class LotReadSchema(BaseModel):
    id: UUID
    price: int
    min_price_step: int
    lot_status: LotStatus
    ending_at: datetime
    created_at: datetime


class LotCreateSchema(BaseModel):
    price: int
    duration_minutes: int = Field(ge=1)
    min_price_step: int = Field(ge=10)


class LotCreatedOkSchema(BaseModel):
    msg: str = "The lot was created"
