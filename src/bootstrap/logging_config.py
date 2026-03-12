import logging

import structlog

log = structlog.getLogger(__name__)


def setup_logging() -> None:
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.dict_tracebacks,
            structlog.processors.TimeStamper(utc=True),
            structlog.processors.JSONRenderer(),

        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False
    )


def log_run_app() -> None:
    log.info("RUN_APP")

def log_domain_error(error_code: str, status_code: int, path: str) -> None:
    log.info(
        "DOMAIN_ERROR",
        error_code=error_code,
        status_code=status_code,
        path=path
    )


def log_unexpected_error(path: str, exc_info: Exception) -> None:
    log.error(
        "UNEXPECTED_ERROR",
        path=path,
        exc_info=exc_info
    )

def log_request(
    method: str,
    path: str,
    duration_ms: int,
    client_ip,
    user_agent: str,
    status_code: str | None = None
) -> None:
    log.info(
        "HTTP_REQUEST",
        method=method,
        path=path,
        status_code=status_code,
        duration_ms=duration_ms,
        client_ip=client_ip,
        user_agent=user_agent
    )
