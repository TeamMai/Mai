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
from typing import Optional, Union

import discord
import PycordUtils
from discord.ext import commands
from discord.ext.commands import BucketType, Bot
from tortoise.expressions import F

from db.models import Guild, Invite
from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log


class Invites(
    Cog,
    name="Invite Manager",
    description="See Who Really Invited Who.",
    emoji=Emoji.LINK,
):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.tracker = PycordUtils.InviteTracker(bot)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.tracker.cache_invites()
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite) -> None:
        await self.tracker.update_invite_cache(invite)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        await self.tracker.add_guild_cache(guild)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite: discord.Invite) -> None:
        await self.tracker.remove_invite_cache(invite)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        await self.tracker.remove_guild_cache(guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        pass

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        return

        if member.bot:
            return

        inviter = await self.tracker.fetch_inviter(member)

        if not inviter:
            return

        guild = (await Guild.get_or_create(discord_id=member.guild.id))[0]

        record, created_new = await Invite.get_or_create(
            inviter_id=inviter.id,
            guild=guild,
            defaults={"invite_count_total": 1},
        )

        max_account_age = record.max_account_age

        invite_log_channel_id = record.channel_id

        if invite_log_channel_id is None:
            mai_category = await member.guild.create_category_channel(name="Mai")
            invite_channel = await member.guild.create_text_channel(
                name="invite-logs",
                reason="[MAI] Created Because Invite Channel is not saved in the DB",
                category=mai_category,
            )

        created_at = (
            member.created_at
            - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
        ).days

        if created_at < max_account_age:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} {member.mention} Invite Cannot Be Validated Because Users Account Age Is Less Than Set Max Account Age",
            )
            await invite_channel.send(embed=embed)
            return

        if not created_new:
            record.invite_count_total = F("invite_count_total") + 1
            await record.save(update_fields=["invite_count_total"])
            await record.refresh_from_db(fields=["invite_count_total"])

        embed = discord.Embed(
            color=Colors.SUCCESS,
            description=f"{inviter.mention} has Invited {member.mention}, they now have a total of `{record.invite_count_total}` Invites!",
        )
        embed.set_author(name=str(member), icon_url=member.avatar.url)
        # await invite_channel.send(embed=embed)

    @commands.group(
        name="invites",
        invoke_without_subcommand=True,
        description="Invite Commands",
    )
    @commands.guild_only()
    async def invites(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if member is None:
            member = ctx.author

        if member.bot:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} {member.mention} Cannot Have Invites, Reason: `User Is Bot Account`.",
            )
            await ctx.send(embed=embed)
            return

        guild = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]
        invite_user = (await Invite.get_or_create(inviter_id=member.id, guild=guild))[0]

        invites_total = invite_user.invite_count_total
        invites_bonus = invite_user.invite_count_bonus
        invites_left = invite_user.invite_count_left

        embed = discord.Embed(
            color=Colors.SUCCESS,
            description=f"{member.mention} has `{invites_total}`(`{invites_bonus}` bonus, `{invites_left}` left)",
        )
        embed.set_author(name=str(member), icon_url=member.avatar.url)
        await ctx.send(embed=embed)

    @invites.command(name="leaderboard", aliases=["lb"])
    async def invites_leaderboard(self, ctx: commands.Context) -> None:
        pass

    @commands.has_guild_permissions(manage_guild=True)
    @invites.command(name="add")
    async def invites_add(self, ctx: commands.Context, amount: int) -> None:
        pass

    @commands.has_guild_permissions(manage_guild=True)
    @invites.command(name="delete")
    async def invites_delete(
        self, ctx: commands.Context, type: str, amount: int
    ) -> None:
        pass

    @commands.has_guild_permissions(manage_guild=True)
    @invites.command(name="reset")
    async def invites_reset(
        self,
        ctx: commands.Context,
        member: Optional[Union[discord.Member, str]],
    ) -> None:
        pass

    @invites.group(name="bonus", invoke_without_subcommand=True)
    async def bonus(self, ctx: commands.Context) -> None:
        pass

    @commands.has_guild_permissions(manage_guild=True)
    @bonus.command(name="add")
    async def invites_addbonus(
        self,
        ctx: commands.Context,
        member: Optional[discord.Member],
        amount: int,
    ) -> None:
        pass

    @commands.has_guild_permissions(manage_guild=True)
    @invites.command(name="remove")
    async def invites_removebonus(
        self,
        ctx: commands.Context,
        member: Optional[discord.Member],
        amount: int,
    ) -> None:
        pass

    @invites.group(name="settings")
    async def settings(self, ctx: commands.Context) -> None:
        pass

    @commands.has_guild_permissions(manage_guild=True)
    @settings.command(name="accountage")
    async def invites_setaccountage(self, ctx: commands.Context, age: int) -> None:
        pass

    @commands.has_guild_permissions(manage_guild=True)
    @settings.command(name="channel")
    async def invites_setchannel(
        self, ctx: commands.Context, channel: discord.TextChannel
    ) -> None:
        pass


def setup(bot):
    bot.add_cog(Invites(bot))
