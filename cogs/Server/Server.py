"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import datetime
from typing import Optional

import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot, BucketType

from config.ext.parser import config
from db.models import Guild
from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log
from helpers.types import *


class Server(
    Cog,
    name="Server",
    description="Manage how Mai interacts with your server",
    emoji=Emoji.DISCORD_EMPLOYEE,
):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.group(invoke_without_command=True, description="Manage Server Prefix")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    async def prefix(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            guild: Guild = await Guild.c_get_or_none_by_discord_id(ctx.guild.id)
            prefix = guild.prefix
            embed: Embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"{ctx.author.mention}, My current prefix is `{prefix}` or {self.bot.user.mention}",
            )
            await ctx.send(embed=embed)

    @prefix.command(
        name="set",
        description="set the server prefix for mai",
        extras={"Examples": "prefix set !\nprefix set $$"},
    )
    @commands.has_permissions(administrator=True)
    async def prefix_set(self, ctx: commands.Context, prefix: Optional[str]) -> None:

        if prefix is None:
            embed: Embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} Please Provide a Prefix.",
            )
            await ctx.send(embed=embed, delete_after=15)
            return

        guild: Guild = await Guild.c_get_or_none_by_discord_id(ctx.guild.id)

        if prefix == guild.prefix:
            embed: Embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"My prefix for `{ctx.guild.name}` is already `{prefix}`!",
            )
            await ctx.send(embed=embed)
            return

        if guild is not None:
            guild.prefix = prefix
            await guild.c_save(update_fields=["prefix"])
            self.bot.dispatch(
                "prefix_update",
                "Guild Prefix Updated",
                ctx.guild,
                prefix,
                guild.prefix,
                datetime.datetime.utcnow(),
            )

            embed: Embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"I set your guild's prefix to `{guild.prefix}`",
            )
            await ctx.send(embed=embed)
        else:
            await Guild.create(discord_id=ctx.guild.id, prefix=prefix, language="en")
            embed: Embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"I set your guild's prefix to `{guild.prefix}`",
            )
            await ctx.send(embed=embed)

    @prefix.command(
        name="reset",
        description="set the server prefix for mai",
        extras={"Examples": "prefix reset"},
    )
    @commands.has_permissions(administrator=True)
    async def prefix_reset(self, ctx: commands.Context) -> None:

        guild: Guild = await Guild.c_get_or_none_by_discord_id(ctx.guild.id)
        old_prefix = guild.prefix
        if guild is not None:
            guild.prefix = config["DEFAULT_PREFIX"]
            await guild.c_save(update_fields=["prefix"])
            self.bot.dispatch(
                "prefix_update",
                "Guild Prefix Reset",
                ctx.guild,
                old_prefix,
                "-",
                datetime.datetime.utcnow(),
            )
            embed: Embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"I resetted this guild's prefix to `{guild.prefix}`",
            )
            await ctx.send(embed=embed)
        else:
            await Guild.create(discord_id=ctx.guild.id, prefix="-", language="en")
            embed: Embed = discord.Embed(
                color=Colors.DEFAULT,
                description="Prefix Resetted to default.",
            )
            await ctx.send(embed=embed)


def setup(bot) -> None:
    bot.add_cog(Server(bot))
