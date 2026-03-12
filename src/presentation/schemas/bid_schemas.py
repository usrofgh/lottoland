from datetime import datetime
from uuid import UUID

from pydantic import BaseModel



class BidReadSchema(BaseModel):
    id: UUID
    lot_id: UUID
    bidder: str
    amount: int
    created_at: datetime


class BidCreateSchema(BaseModel):
    bidder: str
    amount: int


class BidCreatedOkSchema(BaseModel):
    msg: str = "The bid was created"
