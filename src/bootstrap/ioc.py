from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from application.commands.create_bid_command import CreateBidCommand
from application.commands.create_lot_command import CreateLotCommand
from application.queries.get_bids_query import GetBidsQuery
from application.queries.get_lots_query import GetActiveLotsQuery
from bootstrap.settings import Settings
from domain.i_interfaces.i_bid_repo import IBidRepository
from domain.i_interfaces.i_event_publisher import IEventPublisher
from domain.i_interfaces.i_lot_repo import ILotRepository
from infrastructure.db.repositories.bid_repository import BidRepository
from infrastructure.db.repositories.lot_repository import LotRepository
from infrastructure.ws.ws_event_publisher import RedisEventPublisher


class DBProvider(Provider):

    @provide(scope=Scope.APP)
    def settings(self) -> Settings:
        return Settings()

    @provide(scope=Scope.APP)
    def engine(self, settings: Settings) -> AsyncEngine:
        return create_async_engine(
            url=settings.db_dsn,
            # echo=True
        )

    @provide(scope=Scope.APP)
    def session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @provide(scope=Scope.REQUEST)
    async def session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncGenerator[AsyncSession]:
        async with session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def lot_repository(self, session: AsyncSession) -> ILotRepository:
        return LotRepository(session)

    @provide(scope=Scope.REQUEST)
    async def bid_repository(self, session: AsyncSession) -> IBidRepository:
        return BidRepository(session)


class CommandProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def event_publisher(self, redis: Redis) -> IEventPublisher:
        return RedisEventPublisher(redis)

    @provide(scope=Scope.REQUEST)
    async def new_lot_command(
        self,
        lot_repository: ILotRepository,
    ) -> CreateLotCommand:
        return CreateLotCommand(lot_repository)

    @provide(scope=Scope.REQUEST)
    async def new_bid_command(
        self,
        bid_repository: IBidRepository,
        lot_repository: ILotRepository,
        event_publisher: IEventPublisher,
        settings: Settings
    ) -> CreateBidCommand:
        return CreateBidCommand(bid_repository, lot_repository, event_publisher, settings)


class QueryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_lots_query(self, session: AsyncSession) -> GetActiveLotsQuery:
        return GetActiveLotsQuery(session)

    @provide(scope=Scope.REQUEST)
    async def get_bids_query(
        self,
        session: AsyncSession,
        lot_repository: ILotRepository
    ) -> GetBidsQuery:
        return GetBidsQuery(session, lot_repository)


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    def redis(self, settings: Settings) -> Redis:
        return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
