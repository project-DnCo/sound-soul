from pydantic import field_validator
from pydantic import SerializationInfo, ValidationInfo
from pydantic import Field
from pydantic import ConfigDict
from pydantic import SerializerFunctionWrapHandler
from pathlib import Path
from pydantic import BaseModel, field_serializer
import asyncio
from discord.ext import commands
from urllib.parse import quote_plus
import discord
from discord.ext.commands import Bot, Context
from typing import Never

from sound_soul import settings
# settings.API_TOKEN
# asyncio.get_event_loop().run_in_executor()
# Bot.__aenter__

# class App:
#     def __init__(self) -> None:
# import sys
# import discord
# import logging
# import logging.handlers

# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# logging.getLogger('discord.http').setLevel(logging.INFO)

# handler = logging.handlers.RotatingFileHandler(
#     filename='discord.log',
#     encoding='utf-8',
#     maxBytes=32 * 1024 * 1024,  # 32 MiB
#     backupCount=5,  # Rotate through 5 files
# )
# dt_fmt = '%Y-%m-%d %H:%M:%S'
# formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

# Assume client refers to a discord.Client subclass...
# Suppress the default configuration since we have our own


# This example requires the 'message_content' intent.


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member | None = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}~')
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar.')
        self._last_member = member


def run() -> None:
    intents = discord.Intents.default()
    intents.message_content = True
    # # discord.Client.run
    # client = discord.Client(intents=intents)
    # client.add_cog
    # # @client.event
    # # async def on_ready():
    # #     print(f'We have logged in as {client.user}')

    # # @client.event
    # # async def on_message(message):
    # #     if message.author == client.user:
    # #         return

    # #     if message.content.startswith('$hello'):
    # #         await message.channel.send('Hello!')
    token = settings.API_TOKEN.get_secret_value()
    bot = Bot('ss>>', intents=intents)
    # Greetings.qualified_name
    # bot.load_extension
    import typing

    @bot.command()
    async def bottles(ctx: Context, amount: typing.Optional[int], *, liquid="beer"):
        await ctx.send(f'{amount} bottles of {liquid} on the wall!')

    @bot.command()
    async def slap(ctx: Context, members: commands.Greedy[discord.User],
                   dd: int = 1, *suka: int, hello: str = 'bliat', reason: str = 'no reason'):
        print(members, suka)
        id_ = 530081417217179660
        slapped = ", ".join((str(x) for x in members) if members else '123')
        await ctx.send(f'{slapped} just got slapped for {reason} - {dd} | {suka} - {hello}')

    @bot.command()
    async def id(ctx: Context) -> None:
        user = bot.get_guild(41771983423143937)
        # user.global_name
        await ctx.send(str(ctx.author.id))
        await ctx.send(user.name if user else 'not found')

    async def predicate(ctx):
        return bool(ctx.guild)
    is_in_guild = commands.check(predicate)

    class SomeType:
        foo: int

        @classmethod
        async def convert(cls, ctx, argument):
            SomeType.foo = argument
            return SomeType()

    @bot.command()
    async def bar(ctx: Context, cool_value: SomeType):
        await ctx.send(repr(cool_value.foo))  # type checker warns MyVeryCoolConverter has no value foo (uh-oh)

    @bot.command()
    @commands.is_owner()
    @is_in_guild
    async def secretguilddata(ctx):
        """super secret stuff"""
        await ctx.send('secret stuff')

    @secretguilddata.error
    async def secretguilddata_error(ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('nothing to see here comrade.')

    @bot.command()
    async def echo(ctx: Context, *, message: str) -> None:
        await ctx.send(message)

    @bot.command()
    async def guildid(ctx: Context) -> None:
        await ctx.send(str(ctx.guild.id) if ctx.guild else 'notaguild')
    bot.run(token)
    # commands.command
    # client.run(token)
    # # client.run(token, log_handler=None)

    # This example requires the 'message_content' privileged intent to function.


class GoogleBot(commands.Bot):
    # Suppress error on the User attribute being None since it fills up later
    user: discord.ClientUser

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


# Define a simple View that gives us a google link button.
# We take in `query` as the query that the command author requests for
class Google(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        # we need to quote the query string to make a valid url. Discord will raise an error if it isn't valid.
        query = quote_plus(query)
        url = f'https://www.google.com/search?q={query}'

        # Link buttons cannot be made with the decorator
        # Therefore we have to manually create one.
        # We add the quoted url to the button, and add the button to the view.
        self.add_item(discord.ui.Button(label='Click Here', url=url))

# import test
# bot = GoogleBot()


# @bot.command()
# async def google(ctx: commands.Context, *, query: str):
#     """Returns a google link for a query"""
#     # ctx.voice_client
#     await ctx.send(f'Google Result for: `{query}`', view=Google(query))


# discord.PCMAudio


# class Audio(BaseModel):
#     HAIL: str

#     @field_validator('*')
#     @classmethod
#     def _expand_path(cls, value: str) -> str:
#         return (Path(__file__).parent.parent.parent / 'audio' / value).as_posix()


# a = Audio(HAIL='hail.m4a')
# print(a, a.HAIL)
# print(a.model_dump(by_alias=True))
run()
