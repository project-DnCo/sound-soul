from typing import Final

import discord
from discord.ext import commands


class Bot(commands.Bot):
    _PREFIX: Final[str] = 'ss>>'
    _ACTIVITY: Final[str] = 'ss>>hail to resonate'

    def __init__(self) -> None:
        discord.utils.setup_logging()  # TODO: customize

        intents = discord.Intents(
            guilds=True,
            guild_messages=True,
            message_content=True,
            voice_states=True,
        )
        super().__init__(self._PREFIX, intents=intents)

    async def on_ready(self) -> None:
        await self.change_presence(activity=discord.CustomActivity(self._ACTIVITY))
