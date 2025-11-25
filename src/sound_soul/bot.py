import asyncio
from typing import Final, Callable

import discord

from . import settings


class Bot(discord.Client):
    _PREFIX: Final[str] = 'ss>>'
    _DISCONNECT_DELAY: Final[int] = 3
    _ACTIVITY: Final[str] = 'ss>>hail to resonate'

    def __init__(self) -> None:
        discord.utils.setup_logging()  # TODO: customize

        intents = discord.Intents(
            guilds=True,
            guild_messages=True,
            message_content=True,
            voice_states=True,
        )
        super().__init__(intents=intents)

    async def on_ready(self) -> None:
        await self.change_presence(activity=discord.CustomActivity(self._ACTIVITY))

    async def on_message(self, message: discord.Message) -> None:
        assert self.user
        if message.author == self.user:
            return
        if not message.content.startswith(self._PREFIX):
            return
        content = message.content[len(self._PREFIX):].rstrip()
        if not content:
            await message.reply('R u retarded or smth?')  # 1
            return
        command, _, *query = content.partition(' ')
        match command:
            case _ if not command:
                await message.reply('bruh')  # 3
            case 'hail':
                await self._hail(message)
            case 'bye':
                await self._stop(message)
            case 'pause':
                await self._pause(message)
            case 'unpause':
                await self._unpause(message)
            case _:
                await message.reply('fuck you')  # 4

    async def _hail(self, message: discord.Message) -> None:
        voice_client = await self._get_voice_client(message, connect=True)
        if not voice_client:
            await message.channel.send('you stupid')  # 2
            return
        if voice_client.is_playing():
            return
        source = discord.FFmpegPCMAudio(settings.audio_files.HAIL)
        voice_client.play(source, after=await self._make_after_hail(message))

    async def _make_after_hail(self, message: discord.Message) -> Callable[[Exception | None], None]:
        event = asyncio.Event()

        def after_hail(exception: Exception | None) -> None:
            event.set()
            print(f'Player error: {exception}') if exception else None
            if exception:
                ...

        asyncio.create_task(self._stop(message, event))
        return after_hail

    async def _pause(self, message: discord.Message) -> None:
        voice_client = await self._get_voice_client(message)
        if not (voice_client and voice_client.is_playing()):
            await message.channel.send('you stupid')  # 5
            return
        voice_client.pause()

    async def _unpause(self, message: discord.Message) -> None:
        voice_client = await self._get_voice_client(message)
        if not (voice_client and voice_client.is_paused()):
            await message.channel.send('you stupid')  # 6
            return
        voice_client.resume()

    async def _get_voice_client(self, message: discord.Message, *, connect: bool = False) -> discord.VoiceClient | None:
        if not message.guild:
            return None
        assert isinstance(message.author, discord.Member)
        voice_channel = message.author.voice and message.author.voice.channel
        voice_client = message.guild.voice_client
        if voice_client:
            assert isinstance(voice_client, discord.VoiceClient)
            if voice_channel and voice_channel != voice_client.channel:
                if connect:
                    await voice_client.move_to(voice_channel)
                else:
                    return None
            return voice_client
        if not (connect and voice_channel):
            return None
        return await voice_channel.connect()

    async def _stop(self, message: discord.Message, event: asyncio.Event | None = None) -> None:
        if event:
            await event.wait()
            await asyncio.sleep(self._DISCONNECT_DELAY)
        voice_client = await self._get_voice_client(message)
        if not voice_client:
            return
        if not (event and voice_client.is_playing()):
            await voice_client.disconnect()
