"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

from typing import Union

import discord
from discord.ext import commands
from discord.ext.commands import Bot, BucketType

from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log
from helpers.types import *
from views.report import ReportDropdown


class Report(
    Cog,
    name="Report",
    description="Report Guilds, Users, or Bugs About Mai",
    emoji=Emoji.REPORT,
):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.command(
        name="report",
        description="Report A Bug, User, or Guild",
        extras={"Examples": "report"},
    )
    async def report(
        self,
        ctx: commands.Context,
    ) -> None:

        view = ReportDropdown(self.bot)

        await ctx.send(view=view)


def setup(bot) -> None:
    bot.add_cog(Report(bot))
