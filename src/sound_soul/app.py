from . import settings, cogs
from .bot import Bot


class App:
    async def run(self) -> None:
        async with Bot() as bot:
            await bot.add_cog(cogs.Main())
            await bot.start(settings.API_TOKEN.get_secret_value())
