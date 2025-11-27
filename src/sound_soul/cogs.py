import asyncio
from typing import Callable, Final

import discord
from discord.ext import commands

from . import settings
from .exceptions import CannotEnsureVoiceException


class Main(commands.Cog):
    _DISCONNECT_DELAY: Final[int] = 3

    @commands.command(name='hail', help='Plays Soul Eater mantra')
    async def _hail(self, ctx: commands.Context) -> None:
        assert isinstance(ctx.voice_client, discord.VoiceClient)
        if ctx.voice_client.is_playing():
            return
        source = discord.FFmpegPCMAudio(settings.audio_files.HAIL)
        ctx.voice_client.play(source, after=await self._make_after_hail(ctx))

    @_hail.before_invoke
    async def _ensure_voice(self, ctx: commands.Context) -> None:
        if not ctx.guild:
            return
        assert isinstance(ctx.author, discord.Member)
        voice_channel = ctx.author.voice and ctx.author.voice.channel
        if ctx.voice_client:
            assert isinstance(ctx.voice_client, discord.VoiceClient)
            if voice_channel and voice_channel != ctx.voice_client.channel:
                await ctx.voice_client.move_to(voice_channel)
        elif not voice_channel:
            raise CannotEnsureVoiceException
        else:
            await voice_channel.connect()

    @_hail.error
    async def _on_hail_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, CannotEnsureVoiceException):
            await ctx.reply(str(error))

    @commands.command(name='bye', help='Disconnects me from voice')
    async def _stop(self, ctx: commands.Context, event: asyncio.Event | None = None) -> None:
        if event:
            await event.wait()
            await asyncio.sleep(self._DISCONNECT_DELAY)
        if not ctx.voice_client:
            return
        assert isinstance(ctx.voice_client, discord.VoiceClient)
        if not (event and ctx.voice_client.is_playing()):
            await ctx.voice_client.disconnect()

    async def _make_after_hail(self, ctx: commands.Context) -> Callable[[Exception | None], None]:
        event = asyncio.Event()

        def after_hail(exception: Exception | None) -> None:
            event.set()
            print(f'Player error: {exception}') if exception else None
            if exception:
                ...

        asyncio.create_task(ctx.invoke(self._stop, event))
        return after_hail
