from contextlib import asynccontextmanager

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from bootstrap.ioc import DBProvider, RepositoryProvider, CommandProvider, QueryProvider, RedisProvider
from bootstrap.logging_config import setup_logging, log_run_app
from domain.errors import DomainError
from infrastructure.tasks.ended_lots_checker import make_check_ended_lots
from presentation.error_handler import unexpected_error_handler, domain_error_handler
from presentation.middlewares import RequestLoggingMiddleware
from presentation.routes.bid_router import bid_router
from presentation.routes.lot_router import lot_router
from presentation.routes.sockets import socket_router


def create_app() -> FastAPI:
    setup_logging()
    log_run_app()

    # SETUP INVERSION OF CONTROL (INSTEAD OF FASTAPI 'Depends')
    ioc = make_async_container(
        DBProvider(),
        RepositoryProvider(),
        CommandProvider(),
        QueryProvider(),
        RedisProvider()
    )

    scheduler = AsyncIOScheduler()  # It's necessary to check ended lots

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        job = await make_check_ended_lots(ioc)
        scheduler.add_job(job, "interval", seconds=30)
        scheduler.start()
        yield
        scheduler.shutdown()


    app = FastAPI(lifespan=lifespan)
    app.add_middleware(RequestLoggingMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ADD HANDLERS
    routers = [lot_router, bid_router, socket_router]
    for r in routers:
        app.include_router(r)

    # ADD EXCEPTION HANDLERS
    app.add_exception_handler(DomainError, domain_error_handler)
    app.add_exception_handler(Exception, unexpected_error_handler)

    setup_dishka(ioc, app)
    return app


if __name__ == "__main__":
    uvicorn.run(
        app=create_app(),
        host="127.0.0.1",
        port=8000,
        access_log=False # We use custom logs
    )
