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
import humanize
from discord.ext import commands
from discord.ext.commands import Bot, BucketType

from db.models import AFKModel, Guild
from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log


class AFK(
    Cog,
    name="AFK",
    description="Let People Know You're Away From Discord",
    emoji=Emoji.AFK,
):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:

        return

        if message.author.bot:
            return

        if message.guild is None:
            return

        guild = (await Guild.get_or_create(discord_id=message.guild.id))[0]

        afk = await AFKModel.get(guild=guild, afk_user_id=message.author.id)

        if await afk.exists(enabled=True):
            nickname = afk.nickname
            await afk.filter(guild=guild, afk_user_id=message.author.id).update(
                enabled=False, message=None
            )

            try:
                await message.author.edit(nick=nickname, reason="[AFK] Disabled AFK.")
            except discord.Forbidden:
                embed = discord.Embed(
                    color=Colors.ERROR_COLOR,
                    description=f"{Emoji.ERROR} **Missing Permissions to edit {message.author.mention}'s nickname.**",
                )
                await message.channel.send(embed=embed)

            embed = discord.Embed(
                color=Colors.SUCCESS_COLOR,
                description=f"{Emoji.CHECKMARK} {message.author.mention}**, Your AFK status has been disabled!**",
            )
            await message.channel.send(embed=embed)

            afk_data_list = await AFK.filter(guild=guild, enabled=True)
            for afk_data in afk_data_list:
                member = await self.bot.fetch_user(afk_data.afk_user_id)
                start_time = afk_data.start_time
                now = datetime.datetime.now(datetime.timezone.utc)
                time = (now - start_time).total_seconds()
                delta = datetime.timedelta(seconds=time)
                humanized_time = humanize.precisedelta(delta, minimum_unit="seconds")
                if member in message.mentions:
                    if not afk_data.message:
                        embed = discord.Embed(
                            color=Colors.EMBED_COLOR,
                            description=f"{member.mention} **Is Currently AFK since** `{humanized_time}` **ago**",
                        )
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            color=Colors.EMBED_COLOR,
                            description=f"{member.mention} **Is Currently AFK:** `{afk_data.message}`, Time: `{humanized_time}` **ago**",
                        )
                        await message.channel.send(embed=embed)

    @commands.command(
        name="AFK", description="Go AFK", extras={"Examples": "going to walk my dog"}
    )
    @commands.cooldown(1, 10, BucketType.user)
    async def afk(self, ctx: commands.Context, *, afk_message: Optional[str]) -> None:
        if afk_message is None:
            embed = discord.Embed(
                color=Colors.ERROR_COLOR,
                description=f"{Emoji.ERROR} Please Provide An AFK Message",
            )
            await ctx.send(embed=embed, delete_after=15)
            return

        previous_nickname = ctx.author.display_name

        if "[AFK]" in previous_nickname:
            return

        afk_nickname = f"[AFK]{previous_nickname}"

        guild = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]

        afk = await AFKModel.get(guild=guild, afk_user_id=ctx.author.id)

        if afk.exists(enabled=True):
            await afk.filter(guild=guild, afk_user_id=ctx.author.id).update(
                enabled=False, message=None
            )
            embed = discord.Embed(
                color=Colors.SUCCESS_COLOR,
                description=f"{Emoji.WHITE_CHECKMARK} Welcome Back!",
            )
            await ctx.send(embed=embed, delete_after=5)
            return

        await afk.update_or_create(
            guild=guild,
            afk_user_id=ctx.author.id,
            enabled=True,
            message=afk_message,
            nickname=previous_nickname,
        )

        try:
            await ctx.author.edit(nick=afk_nickname, reason=f"[AFK] Disabled AFK.")
        except discord.Forbidden:
            embed = discord.Embed(
                color=Colors.ERROR_COLOR,
                description=f"{Emoji.ERROR} **Missing Permissions to edit {ctx.author.mention}'s nickname.**",
            )
            await ctx.send(embed=embed)

        embed = discord.Embed(
            color=Colors.SUCCESS_COLOR,
            description=f"{Emoji.WHITE_CHECKMARK} Successfully Went AFK: {afk_message}",
        )
        await ctx.send(embed=embed, delete_after=30)

    @commands.command()
    async def create_guild(self, ctx: commands.Context) -> None:
        await Guild.create(discord_id=ctx.guild.id)
        await ctx.send("done.")


def setup(bot):
    bot.add_cog(AFK(bot))
