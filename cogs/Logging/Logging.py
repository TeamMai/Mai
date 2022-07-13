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
from discord.ext.tasks import T
import humanize

from typing import Optional, Union
from tortoise.exceptions import DoesNotExist, IntegrityError
from datetime import datetime

from discord.ext import commands
from discord.ext.commands import BucketType, Greedy
from discord import AuditLogAction, AuditLogEntry

from helpers.constants import *
from helpers.logging import log
from helpers.formatting import format_logging_model
from helpers.custommeta import CustomCog as Cog

from db.models import Guild, ServerLogging


class Logging(
    Cog, name="Logging", description="Manage Server Logging", emoji=":pencil:"
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    async def get_audit_log_entry(
        self,
        guild: discord.Guild,
        action: AuditLogAction,
        target: discord.abc.Snowflake,
    ) -> Optional[AuditLogEntry]:
        """Retrieves an audit log entry that affected a specified entity.

        Parameters
        ----------
        guild : discord.Guild
            The guild to search logs for
        action : AuditLogAction
            The type of action to look for
        target : discord.abc.Snowflake
            The entity that was affected by this action

        Returns
        -------
        Optional[AuditLogEntry]
            The entry that was found or None if there is no entry matching requested conditions
        """
        entry = await guild.audit_logs(action=action).find(
            lambda entry: entry.target.id == target.id
        )
        return entry

    async def get_logs_channel(
        self, guild: Union[discord.Guild, int]
    ) -> discord.TextChannel:
        """Get The Logging Channel Of A Guild

        Parameters
        ----------
        guild : Union[discord.Guild, int]
            The Guild To Find The Channel For

        Returns
        -------
        [discord.TextChannel]
            The Logging Channel
        """
        guild_id = guild.id if type(guild) is discord.Guild else int(guild)

        guild_model = (await Guild.get_or_create(discord_id=guild_id))[0]

        logging = await ServerLogging.get(guild=guild_model)

        if logging.enabled:
            logging_channel_id = logging.channel_id

            text_channels = (
                self.bot.get_guild(guild).text_channels
                if type(guild) is int
                else guild.text_channels
            )

            logging_channel = discord.utils.get(
                text_channels, id=logging_channel_id
            )
            if logging_channel is None:
                pass
            else:
                return logging_channel
        else:
            return

    async def get_logging_model(self, guild_id: int) -> ServerLogging:
        """Get The Guild's Logging Model

        Parameters
        ----------
        guild_id : int
            ID of the Guild

        Returns
        -------
        [ServerLogging]
            The Specified Guild Model
        """
        guild = (await Guild.get_or_create(discord_id=guild_id))[0]

        logging_model = (await ServerLogging.get_or_create(guild=guild))[0]

        return logging_model

    @commands.group(
        invoke_without_subcommand=True, description="Manage Logging"
    )
    @commands.guild_only()
    async def logging(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)
            return

    @commands.cooldown(1, 2, BucketType.user)
    @logging.command(
        name="toggle",
        description="Toggle Logging on/off",
        extras={"Examples": "logging toggle on\nlogging toggle off\nlogging toggle True\nlogging toggle False"},
    )
    async def logging_toggle(
        self, ctx: commands.Context, toggle: Union[str, bool]
    ):

        guild = await Guild.from_context(ctx)

        logging = await ServerLogging.get_or_none(guild=guild)

        if type(toggle) is str:
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

        logging.enabled = toggle
        await logging.save(update_fields=["enabled"])
        await logging.refresh_from_db(fields=["enabled"])

        embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"**Logging Toggled To:** `{toggle}`",
        )

        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, BucketType.user)
    @logging.command(
        name="channel",
        description="Set the channel used for logging",
        extras={"Examples": "logging channel 1234567\nlogging channel #channel(mention)"},
    )
    async def logging_channel(
        self, ctx: commands.Context, channel: Union[discord.TextChannel, int]
    ):
        channel_id = (
            channel.id if type(channel) is discord.TextChannel else int(channel)
        )

        guild = await Guild.from_context(ctx)

        logging = await ServerLogging.get_or_none(guild=guild)

        logging.channel_id = channel_id

        await logging.save(update_fields=["channel_id"])
        await logging.refresh_from_db(fields=["channel_id"])

        channel = ctx.guild.get_channel(channel_id)

        embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"**Logging Channel Updated Too:** {channel.mention}",
        )

        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, BucketType.user)
    @logging.command(
        name="view",
        description="View all enabled/disabled logs",
    )
    async def logging_view(self, ctx: commands.Context):
        loading_embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"{Emoji.LOADING_CIRCLE} Fetching Stats...",
        )
        message = await ctx.send(embed=loading_embed)

        guild = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]

        logging = await ServerLogging.get(guild=guild)
        await message.edit(content=None, embed=format_logging_model(logging))

    @commands.cooldown(1, 2, BucketType.user)
    @logging.command(
        name="set",
        aliases=["add"],
        description="Set Which Events Should Be Logged",
        extras={"Examples": "`logging set message_edited True`\n`logging set message_edited on`\n\n**All Possible Sets**\n`message_edited`\n`message_deleted`\n`nickname_changed`\n`member_updated`\n`member_banned`\n`member_unbanned`\n`member_joined`\n`member_left`\n`role_created`\n`role_updated`\n`role_deleted`\n`member_roles_changed`\n`member_joined_voice_channel`\n`member_left_voice_channel`\n`server_edit`\n`server_emojis_updated`\n`channel_created`\n`channel_updated`\n`channel_deleted`"},
    )
    async def logging_set(
        self,
        ctx: commands.Context,
        log: Optional[str],
        toggle: Optional[Union[str, bool]],
    ):

        if log not in ValidTypes.Logging:
            await ctx.send_help(ctx.command)

        else:
            guild = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]

            logging = await ServerLogging.get(guild=guild)

            setattr(logging, log, toggle)

            await logging.save(update_fields=[log])
            await logging.refresh_from_db(fields=[log])

            embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"{Emoji.CHECKMARK} `{log}` **Has Been Successfully Updated Too** `{toggle}`",
            )

            await ctx.send(embed=embed)

    @commands.cooldown(1, 2, BucketType.user)
    @logging.command(
        name="ignore",
        description="Set Channels To Be Ignored From Logging",
        extras={"Examples": "`logging ignore #mychannel`\n`logging ignore #mychannel1 #mychannel2 #mychannel3`"},
    )
    async def logging_ignore(
        self, ctx: commands.Context, channels: Greedy[discord.TextChannel]
    ):
        if not channels:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} No Valid Channels Were Provided",
            )
            await ctx.send(embed=embed)
            return

        guild = await Guild.from_context(ctx)

        already_ignored_channels = []

        new_ignored_channels = []

        for channel in channels:
            ignored, exists = await ServerLogging.get_or_create(  # FIXME
                guild=guild, ignored_logging_channels=channel.id
            )
            if not exists:
                already_ignored_channels.append(channel)
            else:
                new_ignored_channels.append(channel)

        if already_ignored_channels:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{', '.join([channel.mention for channel in already_ignored_channels])} Is Already Being Ignored.",
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            color=Colors.SUCCESS,
            description=f"{', '.join([channel.mention for channel in new_ignored_channels])} Are Now Being Ignored.",
        )
        await ctx.send(embed=embed)
        await ctx.message.add_reaction(Emoji.CHECKMARK)

    @commands.Cog.listener()
    async def on_message_edit(
        self, before: discord.Message, after: discord.Message
    ):

        logging = await self.get_logging_model(guild_id=before.guild.id)

        if (
            logging.message_edited is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            member = before.author

            if member.bot:
                if logging.log_actions_by_bots == False:
                    pass
                else:
                    return

            if before.content == after.content:
                return

            embed = discord.Embed(
                color=Colors.DEFAULT,
                timestamp=datetime.utcnow(),
                description=f":pencil: [Message]({before.jump_url}) Sent By {member.mention} Edited In {before.channel.mention}",
            )
            embed.set_author(name=str(member), icon_url=member.avatar.url)
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Old Message", value=f"`{before.content}`")
            embed.add_field(name="New Message", value=f"`{after.content}`")
            log_channel = await self.get_logs_channel(before.guild.id)
            await log_channel.send(embed=embed)
        else:
            return

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):

        logging = await self.get_logging_model(guild_id=message.guild.id)

        if (
            logging.message_deleted is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            member = message.author

            if member.bot:
                if logging.log_actions_by_bots == False:
                    pass
                else:
                    return

            embed = discord.Embed(
                color=Colors.DEFAULT,
                timestamp=datetime.utcnow(),
                description=f":wastebasket: Message Sent By {member.mention} Deleted In {message.channel.mention}",
            )

            if message.content == "":
                return

            embed.set_author(name=str(member), icon_url=member.avatar.url)
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Deleted Message", value=f"{message.content}")
            embed.set_footer(text=f"ID: {member.id} | Message ID: {message.id}")
            log_channel = await self.get_logs_channel(message.guild.id)
            await log_channel.send(embed=embed)
        else:
            return

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        logging = await self.get_logging_model(member.guild.id)

        if (
            logging.member_joined is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            if member.bot:
                if logging.log_actions_by_bots == False:
                    pass
                else:
                    return

            embed = discord.Embed(
                color=Colors.DEFAULT,
                timestamp=datetime.utcnow(),
                description=f":e_mail: {member.mention} Has Joined The Server",
            )
            embed.set_author(name=str(member), icon_url=member.avatar.url)
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=f"ID: {member.id}")
            log_channel = await self.get_logs_channel(member.guild.id)
            await log_channel.send(embed=embed)
        else:
            return

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):

        logging = await self.get_logging_model(member.guild.id)

        if (
            logging.member_left is True
            and logging.enabled != True
            and logging.channel_id is not None
        ):

            if member.bot:
                if logging.log_actions_by_bots == False:
                    pass
                else:
                    return

            embed = discord.Embed(
                color=Colors.DEFAULT,
                timestamp=datetime.utcnow(),
                description=f"{member.mention} | {member.name}",
            )
            total_roles = [role.mention for role in member.roles]
            roles = total_roles[1:]
            roles = roles[::-1]
            embed.set_author(name="Member Left", icon_url=member.avatar.url)
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Roles", value=" ".join(roles), inline=False)
            embed.set_footer(text=f"ID: {member.id}")
            log_channel = await self.get_logs_channel(member.guild.id)
            await log_channel.send(embed=embed)
        else:
            return

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):

        return

        # FIXME: cannot get guild because discord.User has no guild, patch soon.

        logging = await self.get_logging_model(before.guild.id)

        if (
            logging.member_updated is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            if before.bot:
                if logging.log_actions_by_bots == False:
                    pass
                else:
                    return

            if before.avatar.url != after.avatar.url:
                embed = discord.Embed(
                    color=Colors.DEFAULT,
                    timestamp=datetime.utcnow(),
                    description=f"{after.mention} **Updated Their Profile.**",
                )
                embed.set_author(name=after.name, icon_url=after.avatar.url)
                embed.set_thumbnail(url=after.avatar.url)
                embed.add_field(
                    name="Avatar",
                    value=f"[[before]]({before.avatar.url}) -> [[after]]({after.avatar.url})",
                )
                embed.set_footer(text=f"ID: {after.id}")
                log_channel = await self.get_logs_channel(before.guild.id)
                await log_channel.send(embed=embed)

            if before.name != after.name:
                embed = discord.Embed(
                    color=Colors.DEFAULT,
                    timestamp=datetime.utcnow(),
                    description=f"{after.mention} **Updated Their Profile.**",
                )
                embed.set_author(name=after.name, icon_url=after.avatar.url)
                embed.set_thumbnail(url=after.avatar.url)
                embed.add_field(
                    name="Username",
                    value=f"**{before.name}** -> **{after.name}**",
                )
                embed.set_footer(text=f"ID: {after.id}")
                log_channel = await self.get_logs_channel()
                await log_channel.send(embed=embed)

            if before.discriminator != after.discriminator:
                embed = discord.Embed(
                    color=Colors.DEFAULT,
                    timestamp=datetime.utcnow(),
                    description=f"{after.mention} **Updated Their Profile.**",
                )
                embed.set_author(name=after.name, icon_url=after.avatar.url)
                embed.set_thumbnail(url=after.avatar.url)
                embed.add_field(
                    name="Discriminator",
                    value=f"**#{before.discriminator}** -> **#{after.discriminator}**",
                )
                embed.set_footer(text=f"ID: {after.id}")
                log_channel = await self.get_logs_channel()
                await log_channel.send(embed=embed)
        else:
            return

    @commands.Cog.listener()
    async def on_member_update(
        self, before: discord.Member, after: discord.Member
    ):

        logging = await self.get_logging_model(before.guild.id)

        if (
            logging.member_updated is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            if before.bot:
                if logging.log_actions_by_bots == False:
                    pass
                else:
                    return

            if before.nick != after.nick:
                embed = discord.Embed(
                    color=Colors.DEFAULT,
                    timestamp=datetime.utcnow(),
                    description=f":pencil: {after.mention} **Nickname Edited.**",
                )
                embed.set_author(name=after.name, icon_url=after.avatar.url)
                embed.set_thumbnail(url=after.avatar.url)
                embed.add_field(name="Old Nickname", value=f"`{before.nick}`")
                embed.add_field(name="New Nickname", value=f"`{after.nick}`")
                embed.set_footer(text=f"ID: {after.id}")
                log_channel = await self.get_logs_channel()
                await log_channel.send(embed=embed)
            if len(before.roles) < len(after.roles):
                log_channel = await self.get_logs_channel(before.guild.id)
                embed = discord.Embed(
                    color=Colors.DEFAULT,
                    timestamp=datetime.utcnow(),
                    description=f"{Emoji.MEMBERS} {before.mention} **Roles Updated**",
                )
                embed.set_author(name=after.name, icon_url=after.avatar.url)
                embed.set_thumbnail(url=after.avatar.url)

                mentions = [role.mention for role in before.roles]
                OldRoles = mentions[1:]

                newRole = next(
                    role for role in after.roles if role not in before.roles
                )

                embed.add_field(name="Old Roles", value=f"{OldRoles}")
                embed.add_field(name="New Role", value=newRole.mention)
        else:
            return

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        logging = await self.get_logging_model(guild.id)

        if (
            logging.member_banned is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            if user.bot:
                if logging.log_actions_by_bots == False:
                    pass
                else:
                    return

            embed = discord.Embed(
                color=Colors.DEFAULT, description=f"{user.mention} {user}"
            )
            embed.set_author(name="Member Banned", url=user.avatar.url)
            embed.set_thumbnail(url=user.avatar.url)
            embed.set_footer(text=f"ID: {user.id}", icon_url=guild.icon.url)

            log_channel = await self.get_logs_channel(guild.id)

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        logging = await self.get_logging_model(guild.id)

        if (
            logging.member_unbanned is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            if user.bot:
                if logging.log_actions_by_bots == False:
                    pass
                else:
                    return

            embed = discord.Embed(
                color=Colors.DEFAULT, description=f"{user.mention} {user}"
            )
            embed.set_author(name="Member UnBanned", url=user.avatar.url)
            embed.set_thumbnail(url=user.avatar.url)
            embed.set_footer(text=f"ID: {user.id}", icon_url=guild.icon.url)

            log_channel = await self.get_logs_channel(guild.id)

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):

        logging = await self.get_logging_model(role.guild.id)

        if (
            logging.role_created is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"Role: **{role.name}** Created\n\n{Chars.ARROW} **Name:** {role.mention}\n{Chars.ARROW} **Color:** {role.color}\n{Chars.ARROW} **Hoisted:** {role.hoist}\n{Chars.ARROW} **Mentionable:** {role.mentionable}",
            )
            embed.set_thumbnail(url=role.guild.icon.url)
            embed.set_author(name=role.guild.name, icon_url=role.guild.icon.url)
            embed.set_footer(
                text=f"ID: {role.id}", icon_url=role.guild.icon.url
            )

            log_channel = await self.get_logs_channel(role.guild.id)

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):

        logging = await self.get_logging_model(role.guild.id)

        if (
            logging.role_created is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"Role: **{role.name}** Deleted\n\n{Chars.ARROW} **Name:** {role.mention}\n{Chars.ARROW} **Color:** {role.color}\n{Chars.ARROW} **Hoisted:** {role.hoist}\n{Chars.ARROW} **Mentionable:** {role.mentionable}",
            )
            embed.set_thumbnail(url=role.guild.icon.url)
            embed.set_author(name=role.guild.name, icon_url=role.guild.icon.url)
            embed.set_footer(
                text=f"ID: {role.id}", icon_url=role.guild.icon.url
            )

            log_channel = await self.get_logs_channel(role.guild.id)

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(
        self, before: discord.Role, after: discord.Role
    ):
        logging = await self.get_logging_model(before.guild.id)

        if (
            logging.role_updated is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"Role: **{before.name}** Updated\n\n{Chars.ARROW} **Name:** {before.mention} -> {after.mention}\n{Chars.ARROW} **Color:** `{before.color}` -> `{after.color}`\n{Chars.ARROW} **Hoisted:** `{before.hoist}` -> `{after.hoist}`\n{Chars.ARROW} **Mentionable:** `{before.mentionable}` -> `{after.mentionable}`",
            )
            embed.set_thumbnail(url=before.guild.icon.url)
            embed.set_author(
                name=before.guild.name, icon_url=before.guild.icon.url
            )
            embed.set_footer(
                text=f"ID: {before.id}", icon_url=before.guild.icon.url
            )

            log_channel = await self.get_logs_channel(before.guild.id)

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):

        logging = await self.get_logging_model(member.guild.id)

        if before.channel is None:
            if (
                logging.member_joined_voice_channel is True
                and logging.enabled != False
                and logging.channel_id is not None
            ):

                pass
        elif before.channel is not None:
            if (
                logging.member_left_voice_channel is True
                and logging.enabled != False
                and logging.channel_id is not None
            ):

                pass
        else:
            return

    @commands.Cog.listener()
    async def on_guild_update(
        self, before: discord.Guild, after: discord.Guild
    ):
        return

        logging = await self.get_logging_model(before.id)

        if (
            logging.server_edited is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"{before.name} Has Been Updated",
            )
            embed.set_thumbnail(url=after.icon.url)
            embed.set_author(name=after.name, icon_url=after.icon.url)
            embed.set_footer(text=f"ID: {before.id}", icon_url=after.icon.url)

            # TODO

    @commands.Cog.listener()
    async def on_guild_emojis_update(
        self, guild: discord.Guild, before: discord.Emoji, after: discord.Emoji
    ):

        logging = await self.get_logging_model(guild.id)

        if (
            logging.server_emojis_updated is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            pass

    @commands.Cog.listener()
    async def on_guild_stickers_update(
        self,
        guild: discord.Guild,
        before: discord.GuildSticker,
        after: discord.GuildSticker,
    ):
        logging = await self.get_logging_model(guild.id)

        if (
            logging.server_stickers_updated is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            pass

    @commands.Cog.listener()
    async def on_webhooks_update(self, channel: discord.TextChannel):
        logging = await self.get_logging_model(channel.guild.id)

        if (
            logging.server_webhooks_updated is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            pass

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):

        logging = await self.get_logging_model(channel.guild.id)

        if (
            logging.channel_created is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):

        logging = await self.get_logging_model(channel.guild.id)

        if (
            logging.channel_deleted is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            pass

    @commands.Cog.listener()
    async def on_guild_channel_update(
        self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel
    ):

        logging = await self.get_logging_model(before.guild.id)

        if (
            logging.channel_updated is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            pass

    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite):
        logging = await self.get_logging_model(invite.guild.id)

        if (
            logging.invite_created is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            pass

    @commands.Cog.listener()
    async def on_invite_delete(self, invite: discord.Invite):
        logging = await self.get_logging_model(invite.guild.id)

        if (
            logging.invite_deleted is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            pass

    @commands.Cog.listener()
    async def on_stage_instance_create(
        self, stage_instance: discord.StageInstance
    ):
        logging = await self.get_logging_model(stage_instance.guild.id)

        if (
            logging.stage_created is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            pass

    @commands.Cog.listener()
    async def on_stage_instance_delete(
        self, stage_instance: discord.StageInstance
    ):
        logging = await self.get_logging_model(stage_instance.guild.id)

        if (
            logging.stage_deleted is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            pass

    @commands.Cog.listener()
    async def on_stage_instance_update(
        self, stage_instance: discord.StageInstance
    ):
        logging = await self.get_logging_model(stage_instance.guild.id)

        if (
            logging.stage_updated is True
            and logging.enabled != False
            and logging.channel_id is not None
        ):

            pass


def setup(bot):
    bot.add_cog(Logging(bot))
