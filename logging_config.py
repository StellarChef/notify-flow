"""Central logging setup for the whole project.

Called once from main.py, before the app starts serving. Every module gets its
logger with `logging.getLogger(__name__)` and never calls print() - that way the
destination, level and format are decided here, in one place, instead of being
scattered across the code.

Levels used in this project:
    DEBUG    - detail you only want while chasing a bug (off in normal runs)
    INFO     - something expected happened: order saved, user logged in
    WARNING  - something odd but handled: unknown Shoper status, retry
    ERROR    - an operation failed and the user noticed
    CRITICAL - the app cannot keep running
"""

import logging
import os
from logging.config import dictConfig
from pathlib import Path

# Logs land next to the code, in a folder git ignores. Absolute path, because
# the working directory differs between `uvicorn main:app` and Docker.
LOG_DIR = Path(__file__).parent / "logs"

# Overridable without touching code: set LOG_LEVEL=DEBUG in .env when digging.
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

LOGGING_CONFIG = {
    "version": 1,
    # False on purpose. The default (True) mutes every logger created before
    # this config runs - which includes uvicorn's and SQLAlchemy's, so we would
    # lose exactly the records we care about.
    "disable_existing_loggers": False,
    "formatters": {
        # Console stays short: it is read live, while working.
        "console": {
            "format": "%(levelname)-8s %(name)s | %(message)s",
        },
        # The file carries full context. It is read after something already
        # broke, so the extra width pays for itself - especially the line number.
        "file": {
            "format": "%(asctime)s %(levelname)-8s [%(name)s:%(lineno)d] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
            "level": LOG_LEVEL,
        },
        # Everything from LOG_LEVEL up - the full story, errors included.
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file",
            "level": LOG_LEVEL,
            "filename": str(LOG_DIR / "app.log"),
            # Rotation matters: without it the file grows until the disk is full.
            # 5 MB per file, 5 kept -> at most ~25 MB of history.
            "maxBytes": 5_000_000,
            "backupCount": 5,
            # Order data contains Polish characters; without this Windows would
            # write them in the system codepage and mangle them.
            "encoding": "utf-8",
        },
        # Errors only, in their own file. When something goes wrong at 2am you
        # want the failures alone, not 50k INFO lines to grep through.
        "errors": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file",
            "level": "ERROR",
            "filename": str(LOG_DIR / "errors.log"),
            "maxBytes": 5_000_000,
            "backupCount": 5,
            "encoding": "utf-8",
        },
    },
    "loggers": {
        # uvicorn ships its own handlers. Emptying them and letting records
        # propagate to root means uvicorn's output lands in our files too,
        # formatted like everything else, instead of only on the console.
        "uvicorn": {"handlers": [], "propagate": True},
        "uvicorn.error": {"handlers": [], "propagate": True},
        # Silenced because our own middleware in main.py logs requests, with
        # the response time added. Leaving this on would log each request twice.
        "uvicorn.access": {"handlers": [], "propagate": False},
        # SQLAlchemy is chatty. WARNING keeps pool and dialect problems visible
        # without printing every statement. Set to INFO to see the SQL.
        "sqlalchemy.engine": {"level": "WARNING", "handlers": [], "propagate": True},
    },
    # The catch-all: any logger without its own entry above ends up here.
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["console", "file", "errors"],
    },
}


def setup_logging() -> None:
    """Apply the config. Call once, as early as possible in main.py."""
    # Created here rather than at import time: importing a module should not
    # touch the filesystem. The handlers open their files during dictConfig,
    # so the folder has to exist by now.
    LOG_DIR.mkdir(exist_ok=True)
    dictConfig(LOGGING_CONFIG)

    logging.getLogger(__name__).info(
        "Logging ready - level %s, files in %s", LOG_LEVEL, LOG_DIR
    )
