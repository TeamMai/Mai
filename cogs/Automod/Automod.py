"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import discord
from discord.ext import commands
from discord.ext.commands import Bot, BucketType

from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log
from helpers.types import *


class Automod(
    Cog,
    name="Auto Mod",
    description="Keep Your Server Safe From Trolls",
    emoji=Emoji.DISCORD_OFFICIAL_MODERATOR,
):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )


def setup(bot) -> None:
    bot.add_cog(Automod(bot))
