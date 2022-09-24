import discord
from discord.cog import CogMeta
from discord.ext import commands


class EmojiCogMeta(discord.cog.CogMeta):
    def __new__(cls, *args, **kwargs) -> CogMeta:
        name, bases, attrs = args
        attrs["emoji"] = kwargs.pop("emoji", [])

        return super().__new__(cls, name, bases, attrs, **kwargs)


class CustomCog(commands.Cog, metaclass=EmojiCogMeta):
    pass
