from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status

from application.commands.create_bid_command import CreateBidCommand
from application.queries.get_bids_query import GetBidsQuery
from presentation.schemas.bid_schemas import (
    BidCreatedOkSchema,
    BidCreateSchema,
    BidReadSchema,
)

bid_router = APIRouter(
    prefix="/lots/{lot_id}/bids",
    tags=["Bids"]
)


@bid_router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=BidCreatedOkSchema
)
@inject
async def create_bid(
    lot_id: UUID,
    bid_create_schema: BidCreateSchema,
    create_bid_cmd: FromDishka[CreateBidCommand]
):
    await create_bid_cmd(lot_id, **bid_create_schema.model_dump())
    return BidCreatedOkSchema

@bid_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[BidReadSchema]
)
@inject
async def get_bids(
    lot_id: UUID,
    query: FromDishka[GetBidsQuery]
):
    return await query(lot_id)
