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

from db.models import Guild
from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log


class ChangeLogs(
    Cog,
    name="ChangeLogs",
    description="View Changelogs of Mai",
    emoji=Emoji.CHANGELOGS,
):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.group(
        invoke_without_subcommand=True, description="Manage ChangeLog Posts"
    )
    @commands.guild_only()
    async def changelog(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @changelog.command(
        name="toggle",
        description="Toggle ChangeLogs on/off",
        extras={
            "Examples": "changelog toggle on\nchangelog toggle off\nchangelog toggle True\nchangelog toggle False"
        },
    )
    @commands.has_guild_permissions(administrator=True)
    async def changelog_toggle(
        self, ctx: commands.Context, toggle: Union[bool, str]
    ) -> None:

        guild: Guild = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]

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

        guild.changelog_enabled = toggle
        await guild.save(update_fields=["changelog_enabled"])
        await guild.refresh_from_db(fields=["changelog_enabled"])

        embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"**ChangeLog Toggled To:** `{toggle}`",
        )

        await ctx.send(embed=embed)

    @changelog.command(
        name="channel",
        description="Set the channel used for posting changelogs",
        extras={
            "Examples": "changelog channel 1234567\nchangelog channel #channel(mention)"
        },
    )
    @commands.has_guild_permissions(administrator=True)
    async def changelog_channel(
        self, ctx: commands.Context, channel: Union[discord.TextChannel, int]
    ) -> None:
        channel_id: int = (
            channel.id if isinstance(channel, discord.TextChannel) else int(channel)
        )

        guild: Guild = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]

        guild.changelog_channel = channel_id

        await guild.save(update_fields=["changelog_channel"])
        await guild.refresh_from_db(fields=["changelog_channel"])

        channel = ctx.guild.get_channel(channel_id)

        embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"**ChangeLog Channel Updated Too:** {channel.mention}",
        )

        await ctx.send(embed=embed)

    @changelog.command(name="post", hidden=True)
    @commands.is_owner()
    async def changelog_post(self, ctx: commands.Context, *, message: str) -> None:
        for guild in self.bot.guilds:
            model: Guild = (await Guild.get_or_create(discord_id=guild.id))[0]
            if model.changelog_enabled and model.changelog_channel is not None:
                changelog_channel = ctx.guild.get_channel(model.changelog_channel)
                embed = discord.Embed(color=Colors.DEFAULT, description=message)
                await changelog_channel.send(embed=embed)

    @changelog.command(name="list", hidden=True)
    @commands.is_owner()
    async def changelog_list(self, ctx: commands.Context) -> None:
        embed = discord.Embed(color=Colors.SUCCESS, description="hello")
        for guild in self.bot.guilds:
            model: Guild = (await Guild.get_or_create(discord_id=guild.id))[0]
            if model.changelog_enabled and model.changelog_channel is not None:
                changelog_channel = ctx.guild.get_channel(model.changelog_channel)
                embed.add_field(
                    name=guild.name,
                    value=f"Channel: {changelog_channel.mention}",
                )

        await ctx.send(embed=embed)


def setup(bot) -> None:
    bot.add_cog(ChangeLogs(bot))
