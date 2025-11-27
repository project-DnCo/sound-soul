from discord.ext import commands


class CannotEnsureVoiceException(commands.CommandError):
    def __init__(self, message: str = 'You are not connected to a voice channel.') -> None:
        super().__init__(message)
