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
import statcord

from discord.ext import commands

from helpers.constants import *
from helpers.logging import log
from helpers.custommeta import CustomCog as Cog

from config.ext.parser import config


class StatCord(Cog, command_attrs=dict(hidden=True), emoji=Emoji.STATCORD):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.statcord_api_key = config["STATCORD_API_KEY"]
        self.api = statcord.Client(self.bot, self.statcord_api_key)
        self.api.start_loop()

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context) -> None:
        self.api.command_run(ctx)


def setup(bot):
    bot.add_cog(StatCord(bot))
