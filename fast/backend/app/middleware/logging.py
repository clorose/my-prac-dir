# Absolute path: C:\_YHJ\fast\backend\app\middleware\logging.py

import logging
from fastapi import Request

logger = logging.getLogger(__name__)

async def log_requests(request: Request, call_next):
    logger.debug(f"Incoming request: {request.method} {request.url}")
    logger.debug(f"Request headers: {request.headers}")
    response = await call_next(request)
    logger.debug(f"Outgoing response: Status {response.status_code}")
    logger.debug(f"Response headers: {response.headers}")
    return response
