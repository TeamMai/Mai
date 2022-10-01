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
from typing import Union

import discord
from discord.ext import commands
from discord.ext.commands import Bot, BucketType

from db.models import Guild, GuildEvent, ServerLogging
from helpers.constants import *
from helpers.logging import log

from helpers.custommeta import CustomCog as Cog


class Events(Cog, command_attrs=dict(hidden=True), emoji=Emoji.PYCORD):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.Cog.listener()
    async def on_prefix_update(
        self,
        description: str,
        guild: discord.Guild,
        old_prefix: str,
        new_prefix: str,
        timestamp,
    ) -> None:
        guild: Guild = (await Guild.get_or_create(discord_id=guild.id))[0]

        await GuildEvent.create(
            guild=guild,
            description=description,
            old=old_prefix,
            new=new_prefix,
            timestamp=timestamp,
        )

    @commands.Cog.listener()
    async def on_warn_create(
        self,
        guild: discord.Guild,
        warned: discord.Member,
        warner: discord.Member,
        reason: str,
        warn_id: str,
    ) -> None:
        _guild = await Guild.get_or_none(discord_id=guild.id)

        logging: ServerLogging | None = await ServerLogging.get_or_none(guild=_guild)

        channel_id = logging.channel_id

        channel = self.bot.get_channel(channel_id)

        embed = discord.Embed(
            color=Colors.DEFAULT,
            timestamp=datetime.datetime.utcnow(),
            description=f"{Emoji.DISCORD_OFFICIAL_MODERATOR} {warned.mention} Has Been Warned By {warner.mention}",
        )
        embed.set_author(name=warned.name, icon_url=warned.avatar.url)
        embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="Moderator", value=warner.mention)
        embed.add_field(name="Reason", value=reason)
        embed.add_field(name="Warn ID", value=f"`{warn_id}`", inline=False)
        embed.set_footer(icon_url=warner.avatar.url, text=f"Mod ID: {warner.id}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_warn_delete(
        self,
        guild: discord.Guild,
        warned: Union[str, int],
        warner: discord.Member,
    ) -> None:
        _guild = await Guild.get_or_none(discord_id=guild.id)

        logging: ServerLogging | None = await ServerLogging.get_or_none(guild=_guild)

        channel_id = logging.channel_id

        channel = self.bot.get_channel(channel_id)

        warned: str | int = await self.bot.get_or_fetch_user(warned)

        embed = discord.Embed(
            color=Colors.DEFAULT,
            timestamp=datetime.datetime.utcnow(),
            description=f"{Emoji.DISCORD_OFFICIAL_MODERATOR} {warner.mention} Removed All Warns For {warned.mention}",
        )
        embed.set_author(name=warned.name, icon_url=warned.avatar.url)
        embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="Moderator", value=warner.mention)
        embed.set_footer(icon_url=warner.avatar.url, text=f"Mod ID: {warner.id}")
        await channel.send(embed=embed)


def setup(bot) -> None:
    bot.add_cog(Events(bot))
