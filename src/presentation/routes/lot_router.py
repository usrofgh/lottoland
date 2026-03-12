from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status

from application.commands.create_lot_command import CreateLotCommand
from application.queries.get_lots_query import GetActiveLotsQuery
from presentation.schemas.lot_schemas import (
    LotCreatedOkSchema,
    LotCreateSchema,
    LotReadSchema,
)

lot_router = APIRouter(
    prefix="/lots",
    tags=["Lots"],
)


@lot_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[LotReadSchema]
)
@inject
async def get_active_lots(
    query: FromDishka[GetActiveLotsQuery]
):
    records = await query()
    return records


@lot_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=LotCreatedOkSchema
)
@inject
async def create_lot(
    create_lot_schema: LotCreateSchema,
    command: FromDishka[CreateLotCommand],
):
    await command(**create_lot_schema.model_dump())
    return LotCreatedOkSchema
