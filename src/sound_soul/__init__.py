import asyncio

from .settings_ import settings
from .app import App


def main() -> None:
    app = App()
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        pass
