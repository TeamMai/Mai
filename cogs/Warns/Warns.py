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
import uuid
from typing import Optional, Tuple, Union

import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot, BucketType
from PycordUtils.Pagination import AutoEmbedPaginator

from db.models import Guild, Warns
from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log
from helpers.types import *


class Warn(
    Cog,
    name="Warns",
    description="Warn Misbehaving Members",
    emoji=Emoji.DISCORD_OFFICIAL_MODERATOR,
):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.group(
        invoke_without_command=True,
        name="warn",
        description="Warn Members",
        extras={"Examples": "warn @Member misbehaving"},
    )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def warn(
        self,
        ctx: commands.Context,
        member: Optional[discord.Member],
        *,
        reason="No Reason Provided",
    ) -> None:
        if member == ctx.author:
            embed: Embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} Cannot Warn Yourself.",
            )
            await ctx.send(embed=embed, delete_after=15)
            return

        if member is None:
            await ctx.send_help(ctx.command)

        guild: Guild = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]

        if len(reason) > Limitations.MAX_WARNING_REASON:
            embed: Embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} Reason Must Be Below `350` Characters.",
            )
            await ctx.send(embed=embed, delete_after=15)
            return

        warn_id: str = str(uuid.uuid4())

        warn: Warns = await Warns.create(
            guild=guild,
            warned_id=member.id,
            warner_id=ctx.author.id,
            reason=reason,
            warn_id=warn_id,
        )

        self.bot.dispatch(
            "warn_create",
            guild=ctx.guild,
            warned=member,
            warner=ctx.author,
            reason=reason,
            warn_id=warn_id,
        )

        embed: Embed = discord.Embed(
            color=Colors.SUCCESS,
            description=f"{member.mention} has been warned by {ctx.author.mention}",
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar.url)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="ID", value=f"`{warn.warn_id}`")
        await ctx.send(embed=embed)

    @warn.command(
        name="clear",
        description="Clears A Warning Or All Warnings",
        extras={
            "Examples": "warn clear @Member1 (Clears All Warnings)\nwarn clear e7dd76c1-fe47-4fb2-b8dd-1319e802c490 (Clears 1)"
        },
    )
    @commands.has_permissions(manage_messages=True)
    async def clear_warns(
        self, ctx: commands.Context, to_clear: Union[discord.Member, str]
    ) -> None:
        if to_clear is None:
            await ctx.send_help(ctx.command)

        guild: Guild = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]
        embed: Embed = discord.Embed(
            color=Colors.SUCCESS, timestamp=datetime.datetime.utcnow()
        )

        if isinstance(to_clear, discord.Member):
            await Warns.filter(guild=guild, warned_id=to_clear.id).all().delete()
            clear_message: str = f"Cleared warnings for {to_clear.mention}"
        else:
            await Warns.filter(guild=guild, warn_id=to_clear).delete()
            clear_message: str = f"Cleared Warning: `{to_clear}`"

        self.bot.dispatch(
            "warn_delete",
            guild=ctx.guild,
            warned=to_clear.id if isinstance(to_clear, discord.Member) else "None",
            warner=ctx.author,
        )

        embed.add_field(name="Warning Cleared", value=clear_message, inline=False)
        await ctx.send(embed=embed)

    @warn.command(
        name="list",
        aliases=["modlogs", "show", "logs"],
        description="Returns A List Of A Users Total Warns",
        extras={"Examples": "warn list\nwarn list @Member"},
    )
    @commands.has_permissions(manage_messages=True)
    async def warn_list(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if member is None:
            member: MEMBER | None = ctx.author

        guild: Guild = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]
        warns: List[Warns] = await Warns.filter(guild=guild, warned_id=member.id).all()

        if warns:
            total_warns: int = len(warns)
            paginator = AutoEmbedPaginator(ctx, remove_reactions=True)
            await paginator.run(
                [
                    await self.make_warn_embed(warn, page=(page_num, total_warns))
                    for page_num, warn in enumerate(warns)
                ]
            )
        else:
            embed: Embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"{member.mention} Has No Avaliable Warnings",
            )
            await ctx.send(embed=embed)

    async def make_warn_embed(
        self, warn: Warns, page: Optional[Tuple[int, int]] = None
    ) -> discord.Embed:
        """Makes an embed to represent a warning
        Parameters
        ----------
        warn : Warns
            The warn object fetched from the DB
        page : Tuple[int, int], optional
            The warning page info for pagination,
            first element is the current page,
            second element is the total number of pages,
            this should only be passed if you are paginating embeds
        Returns
        -------
        discord.Embed
            The embed representing the warn
        """
        member: USER = await self.bot.fetch_user(warn.warned_id)
        staff: USER = await self.bot.fetch_user(warn.warner_id)
        paginated: bool = page is not None
        embed: Embed = discord.Embed(
            color=Colors.DEFAULT, timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=f"Warns for {member}", icon_url=member.avatar.url)
        embed.add_field(name="Reason", value=f"`{warn.reason}`", inline=False)
        embed.add_field(name="Warned by", value=f"`{str(staff)}`", inline=False)
        if paginated:
            # Add one to offset 0 index
            page_num: int = page[0] + 1
            total_pages: int = page[1]
            embed.set_footer(
                text=f"Page {page_num} of {total_pages} (Warning ID: {warn.warn_id})"
            )
        else:
            embed.set_footer(text=f"Warning ID: {warn.warn_id}")
        return embed


def setup(bot) -> None:
    bot.add_cog(Warn(bot))
