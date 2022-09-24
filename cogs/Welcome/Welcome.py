"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import os

import discord
from discord.ext import commands
from discord.ext.commands import Bot, BucketType
from easy_pil import Editor, Font, Text, load_image_async

from config.ext.parser import ROOT_DIR
from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log


class Welcome(Cog, name="Welcome", description="Welcome Members", emoji=":wave:"):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )


def setup(bot) -> None:
    bot.add_cog(Welcome(bot))
