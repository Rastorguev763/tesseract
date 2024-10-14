import logging
import os
import sys

from loguru import logger

from src.core.settings import settings

if not os.path.exists(settings.LOG_DIRECTORY):
    os.makedirs(settings.LOG_DIRECTORY, exist_ok=True)

logger.remove()
logger.add(sys.stderr, level=settings.LOGGING_LEVEL, enqueue=True)

if settings.LOG_TO_FILE:
    logger.add(
        settings.log_file_path,
        rotation="10 MB",
        retention="30 days",
        level=settings.LOGGING_LEVEL,
        enqueue=True,
    )
    logger.add(
        settings.error_log_file_path,
        rotation="10 MB",
        retention="30 days",
        level="ERROR",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        enqueue=True,
    )


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


logging.basicConfig(handlers=[InterceptHandler()], level=0)

logger.debug("logging is active")
