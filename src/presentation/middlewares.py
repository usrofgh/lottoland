import time
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from structlog.contextvars import bind_contextvars, clear_contextvars

from bootstrap.logging_config import log_request


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        client_ip = request.client.host
        user_agent = request.headers.get("User-Agent")
        bind_contextvars(request_id=request_id)

        response = None
        start = time.time()
        try:
            response = await call_next(request)
        finally:
            status_code = response.status_code if response else None
            duration = time.time() - start
            log_request(
                method=request.method,
                path=request.url.path,
                duration_ms=int(duration * 1000),
                client_ip=client_ip,
                user_agent=user_agent,
                status_code=status_code
            )
            clear_contextvars()
        response.headers["X-Request-ID"] = request_id
        return response
