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
from roblox import Client

from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log
from helpers.types import *


class Roblox(
    Cog,
    name="Roblox",
    description="Get Player Roblox Stats, or Verify Through Roblox",
    emoji=Emoji.ROBLOX,
):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot
        self.client: Client = Client()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )


def setup(bot) -> None:
    bot.add_cog(Roblox(bot))
