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

from helpers.constants import *
from helpers.logging import log
from helpers.custommeta import CustomCog as Cog


from roblox import Client


class Roblox(
    Cog,
    name="Roblox",
    description="Get Player Roblox Stats, or Verify Through Roblox",
    emoji=Emoji.ROBLOX,
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = Client()

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )


def setup(bot):
    bot.add_cog(Roblox(bot))
