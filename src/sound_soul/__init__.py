import asyncio
import signal
import sys
from types import FrameType, TracebackType

from loguru import logger

from .settings_ import settings
from .log import setup_log
from .app import App


def main() -> None:
    signal.signal(signal.SIGINT, _exit)
    sys.excepthook = _excepthook
    asyncio.run(_run())


def _exit(signum: int, frame: FrameType | None, /) -> None:
    exit(0)


def _excepthook(exctype: type[BaseException], value: BaseException, traceback: TracebackType | None, /) -> None:
    # if this fails, the original excepthook is called
    logger.opt(exception=(exctype, value, traceback)).critical('Unrecoverable error occurred.')


async def _run() -> None:
    async with setup_log():
        app = App()
        await app.run()
