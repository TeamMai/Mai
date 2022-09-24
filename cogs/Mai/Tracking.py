"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""
from typing import Optional, Union

import discord
from discord.ext import commands
from discord.ext.commands import Bot, BucketType

from db.models import Users
from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log


class Tracking(
    Cog,
    name="Tracking",
    description="Track your usage of Mai",
    emoji=Emoji.CHECKMARK,
):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context):
        user = (await Users.get_or_create(user_id=ctx.author.id))[0]

        if user.tracking_enabled:
            await user.increment()
        else:
            return

    @commands.group(invoke_without_subcommand=True, description="Manage Tracking")
    @commands.guild_only()
    async def tracking(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)
            return

    @tracking.command(
        name="toggle",
        description="Toggle Tracking on/off",
        extras={
            "Examples": "tracking toggle on\ntracking toggle off\ntracking toggle True\ntracking toggle False"
        },
    )
    async def tracking_toggle(
        self, ctx: commands.Context, toggle: Union[str, bool]
    ) -> None:

        user = await Users.get_or_create(user_id=ctx.author.id)

        if isinstance(toggle, str):
            if toggle == "on":
                toggle = True
            elif toggle == "off":
                toggle = False
            elif toggle != "on" or "off":
                embed = discord.Embed(
                    color=Colors.ERROR,
                    description=f"{Emoji.ERROR} `toggle` expects `on`/`off`, not `{str(toggle)}`",
                )
                await ctx.send(embed=embed)
                return

        user.tracking_enabled = toggle
        await user.save(update_fields=["tracking_enabled"])
        await user.refresh_from_db(fields=["tracking_enabled"])

        embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"**Tracking Toggled To:** `{toggle}`",
        )

        await ctx.send(embed=embed)

    @tracking.command(
        name="view",
        description="View how many commands you've run",
        extras={"Examples": "tracking view\ntracking view @Member"},
    )
    async def tracking_view(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if member is None:
            member = ctx.author

        user = await Users.get(user_id=ctx.author.id)

        embed = discord.Embed(
            color=Colors.SUCCESS,
            description=f"{member.mention}, you've run `{user.commands_run}` commands",
        )
        embed.set_author(name=member.name, icon_url=member.avatar.url)
        embed.set_footer(
            text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar.url
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Tracking(bot))
