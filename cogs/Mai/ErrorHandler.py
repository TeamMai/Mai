"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import traceback

import discord
import humanize
from discord.ext import commands
from discord.ext.commands import Bot, BucketType

from helpers.constants import *


class ErrorHandler(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            retry_after: float = error.retry_after

            precise: str = humanize.precisedelta(
                retry_after, minimum_unit="seconds", format="%0.2f"
            )

            embed = discord.Embed(
                title="Active Cooldown",
                color=Colors.DEFAULT,
                description=f"Please wait `{precise}` before reusing `{ctx.command}`\n\n__**Cooldown Reductions**__\n`•` Buy [Premium](https://google.com) for an **50%** Reduction\n`•` Vote on [top.gg](https://google.com) for a **20%** Reduction\n`•` Join Our [Support Server]({Links.SUPPORT_SERVER_INVITE}) for a **20%** Reduction",
            )
            embed.set_thumbnail(url=ctx.author.avatar.url)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_footer(
                text=f"ID: {ctx.author.id}", icon_url=ctx.author.avatar.url
            )

            await ctx.send(embed=embed)
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} The command `{ctx.prefix}{ctx.command}` was not found!, If you would like this command to be added suggest it in our [support server]({Links.SUPPORT_SERVER_INVITE})",
            )
            embed.set_thumbnail(url=ctx.author.avatar.url)
            embed.set_author(
                name=ctx.author.name,
                url=Links.BOT_DOCUMENTATION_URL,
                icon_url=ctx.author.avatar.url,
            )
            embed.set_footer(
                text=f"ID: {ctx.author.id}", icon_url=ctx.author.avatar.url
            )
            await ctx.send(embed=embed)
        else:
            traceback.print_exception(type(error), error, error.__traceback__)


def setup(bot) -> None:
    bot.add_cog(ErrorHandler(bot))
