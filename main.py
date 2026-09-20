import logging
import time

from fastapi import FastAPI, Request

# Logging is configured FIRST, before anything else is imported or run - any
# module importing logging later then inherits the finished setup.
from logging_config import setup_logging

setup_logging()

from Database.repository import Base
from Database.config_db import db
from Api.api_connection import router as api_router
from Api.webhook import router as webhook_router
from Api.auth import router as auth_router

# __name__ is "main" here, so records show up as "main | ..." and it is obvious
# which module produced them. Every module does the same with its own __name__.
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(api_router)
app.include_router(webhook_router)
app.include_router(auth_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log one line per request: what came in, what went out, how long it took.

    This replaces uvicorn.access (silenced in logging_config) because it adds
    the duration - the number that tells you a query got slow before anyone
    complains.
    """
    started = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        # An unhandled exception never reaches the line below, so it gets its
        # own record. exc_info=True attaches the traceback - without it you get
        # the message and no idea which line raised it.
        duration_ms = (time.perf_counter() - started) * 1000
        logger.exception(
            "%s %s -> unhandled exception after %.1f ms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    duration_ms = (time.perf_counter() - started) * 1000

    # A failed response is not an application error - a 401 on a bad password is
    # normal traffic. Server errors (5xx) are ours, so they are logged louder.
    level = logging.ERROR if response.status_code >= 500 else logging.INFO
    logger.log(
        level,
        "%s %s -> %d (%.1f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


@app.on_event("startup")
def on_startup():
    # create_all only creates MISSING tables - it never alters an existing one.
    # A changed column still needs a drop/create (or a migration tool).
    Base.metadata.create_all(db)
    logger.info("Database schema ready, application started")
