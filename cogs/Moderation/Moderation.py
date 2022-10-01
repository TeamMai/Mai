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

from datetime import datetime
from typing import Optional

from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log
from helpers.types import *


class Moderation(
    Cog,
    name="Moderation",
    description="Moderate Your Discord Server",
    emoji=Emoji.DISCORD_OFFICIAL_MODERATOR,
):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )
        
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, channel: Optional[discord.TextChannel],  amount: int = 0):
        if channel is None:
            channel = ctx.channel

        embed = discord.Embed(
            color=Colors.SUCCESS,
            timestamp=datetime.utcnow(),
            description=f"Cleared {amount} messages in {ctx.channel.mention}"
        )
        embed.set_author(
            name=f"{ctx.author.name} | Type: Clear", icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.add_field(name="Amount", value=f"`{amount}`", inline=False)
        embed.add_field(
            name="Channel", value=f"{channel.mention}", inline=False)
        await channel.purge(limit=amount)
        await channel.send(embed=embed, delete_after=3)


def setup(bot) -> None:
    bot.add_cog(Moderation(bot))
