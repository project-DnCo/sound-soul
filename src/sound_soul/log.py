import inspect
import logging
import sys
from contextlib import asynccontextmanager
from typing import Final, AsyncIterator

import discord
from loguru import logger

from . import settings


class _RedirectHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            logger.level(record.levelname)
        except ValueError:
            logger.level(record.levelname, record.levelno)

        # mby try patching logger with record instead
        for depth, frame_info in enumerate(inspect.stack()):
            if frame_info.filename == record.pathname:
                break

        logger.opt(depth=depth, exception=record.exc_info).log(record.levelname, record.getMessage())


_FILE_MESSAGE_FORMAT: Final[str] = '{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name}:{function}:{line} - {message}'
_TERMINAL_MESSAGE_FORMAT: Final[str] = (
    '<green>{time:HH:mm:ss}</green> | '
    '<level>{level:<8}</level> | '
    '<cyan>{name}:{function}:{line}</cyan> - '
    '<level>{message}</level>'
)


@asynccontextmanager
async def setup_log() -> AsyncIterator[None]:
    discord.utils.setup_logging(handler=_RedirectHandler(), level=0)
    logger.remove()
    if settings.DEBUG:
        logger.add(
            sink=sys.stderr,
            level='DEBUG',
            format=_TERMINAL_MESSAGE_FORMAT,
            enqueue=True,
        )
    else:
        logger.add(
            sink=sys.stderr,
            level='INFO',
            format=lambda r: _TERMINAL_MESSAGE_FORMAT + '\n',  # bypass '\n{exception}' appended by default
            enqueue=True,
        )
        logger.add(
            sink=settings.LOG_DIR / 'err.log',
            level='ERROR',
            format=_FILE_MESSAGE_FORMAT,
            delay=True,
            compression='zip',
            rotation='10 MB',
            enqueue=True,
        )
    try:
        yield
    finally:
        await logger.complete()
