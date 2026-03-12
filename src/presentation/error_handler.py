from starlette.requests import Request
from starlette.responses import JSONResponse

from bootstrap.logging_config import log_domain_error, log_unexpected_error
from domain.errors import DomainError
from domain.errors import ErrorCodes as Ec

"""
Centralized exception handlers to avoid scattering error-handling logic across the codebase
domain_error_handler - maps known DomainErrors to appropriate HTTP status codes
unexpected_error_handler - catches anything else and returns a generic 500 response
"""

_HTTP_CODE_MAPPER: dict[str, int] = {
    Ec.MUST_BE_MORE_THAN_ZERO: 400,
    Ec.LOT_ALREADY_EXISTS: 409,
    Ec.LOT_NOT_FOUND: 404,
    Ec.LOT_IS_ENDED: 409,
}

async def domain_error_handler(request: Request, error: DomainError) -> JSONResponse:
    error_code = error.args[0]
    status_code = _HTTP_CODE_MAPPER.get(error_code, 400)
    log_domain_error(path=request.url.path, error_code=error_code, status_code=status_code)
    return JSONResponse(
        status_code=status_code,
        content={"error": {"error_code": error_code}}
    )


async def unexpected_error_handler(request: Request, error: Exception) -> JSONResponse:
    log_unexpected_error(path=request.url.path, exc_info=error)
    return JSONResponse(
        status_code=500,
        content={"error": {"error_code": "INTERNAL_ERROR"}}
    )
