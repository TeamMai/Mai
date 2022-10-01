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

from config.ext.parser import config
from db.models import Guild
from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log


class Developer(Cog, description="Developer Commands For Mai", command_attrs=dict(hidden=True), emoji=Emoji.DISCORD_EMPLOYEE):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.blacklist_channel_id = config["SERVER_BLACKLIST_CHANNEL_ID"]

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.group(invoke_without_subcommand=False)
    @commands.is_owner()
    @commands.guild_only()
    async def blacklist(self, ctx: commands.Context):
        pass

    @blacklist.command(
        name="add",
        description="Blacklist A Server From Using Mai",
        extras={"Examples": "blacklist add 1234567\nblacklist add My Server Name"},
    )
    async def add(
        self,
        ctx: commands.Context,
        guild: Optional[Union[discord.Guild, int]],
        *,
        reason: str = "No Reason Provided",
    ) -> None:

        if guild is None:
            await ctx.send_help(ctx.command)
            return

        guild_id = guild if isinstance(guild, int) else guild.id
        guild = await Guild.get(discord_id=guild_id)

        if guild.is_bot_blacklisted:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} Guild Already Blacklisted. refer to `-help blacklist remove`",
            )
            await ctx.send(embed=embed)
            return

        else:
            guild.is_bot_blacklisted = True
            await guild.save(update_fields=["is_bot_blacklisted"])
            await guild.refresh_from_db(fields=["is_bot_blacklisted"])
            await Guild.create(blacklisted_reason=reason)

            embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"{Emoji.CHECKMARK} `{guild.discord_id}` Has been  `blacklisted` for `{reason}`",
            )
            channel = self.bot.get_channel(self.blacklist_channel_id)
            message = await channel.send(embed=embed)
            await ctx.message.add_reaction(Emoji.CHECKMARK)
            await message.add_reaction(Emoji.CHECKMARK)

    @blacklist.command(
        name="remove",
        description="Remove A Server Blacklist From Mai",
        extras={
            "Examples": "blacklist remove 1234567\nblacklist remove My Server Name"
        },
    )
    async def remove(self, ctx: commands.Context, guild: Union[discord.Guild, int]):

        if guild is None:
            await ctx.send_help(ctx.command)
            return

        guild_id = guild if isinstance(guild, int) else guild.id
        guild = await Guild.get(discord_id=guild_id)

        if not guild.is_bot_blacklisted:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} Guild Not Blacklisted. refer to `-help blacklist add`",
            )
            await ctx.send(embed=embed)
            return
        else:
            guild.is_bot_blacklisted = False
            await guild.save(update_fields=["is_bot_blacklisted"])
            await guild.refresh_from_db(fields=["is_bot_blacklisted"])

            embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"{Emoji.CHECKMARK} `{guild.discord_id}` Has been successfully removed from `blacklist`",
            )
            channel = self.bot.get_channel(self.blacklist_channel_id)
            message = await channel.send(embed=embed)
            await ctx.message.add_reaction(Emoji.CHECKMARK)
            await message.add_reaction(Emoji.CHECKMARK)

    @blacklist.command(name="list", description="List All Blacklisted Server ID's")
    async def blacklist_list(self, ctx: commands.Context):
        guilds = await Guild.filter(discord_id=ctx.guild.id).all()
        for guild in guilds:
            g_blacklisted = []
            if guild.is_bot_blacklisted:
                g_blacklisted.append(guild.discord_id)
        blacklisted_ids = (
            ", ".join(g_blacklisted)
            if g_blacklisted is not None
            else "`No Blacklisted Servers`"
        )
        embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"**Guild ID's:** {blacklisted_ids}",
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Developer(bot))
