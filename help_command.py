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
import re
from datetime import timedelta
from typing import Any, List, Literal, Mapping, Optional

import discord
import humanize
from discord import Embed
from discord.ext import commands

from config.ext.parser import config
from helpers.constants import *
from helpers.custommeta import CustomCog


class MaiHelpCommand(commands.HelpCommand):
    def command_not_found(self, string: str) -> str:
        return f"{Emoji.ERROR} The command `{self.context.clean_prefix}{string}` was not found!, If you would like this command to be added suggest it in our [support server]({Links.SUPPORT_SERVER_INVITE})"

    def subcommand_not_found(self, command: commands.Command, string: str) -> str:
        return f"{Emoji.ERROR} I don't have the command `{command.qualified_name} {string}`, If you would like this command to be added suggest it in our [support server]({Links.SUPPORT_SERVER_INVITE})"

    async def dispatch_help(self, help_embed: Embed) -> None:
        dest: discord.abc.MessageableChannel = self.get_destination()
        await dest.send(embed=help_embed)

    async def send_error_message(self, error: str) -> None:
        embed: Embed = Embed(
            title="Error :\\", description=f"{error}", color=Colors.ERROR
        )
        await self.dispatch_help(embed)

    async def send_bot_help(
        self, mapping: Mapping[Optional[CustomCog], List[commands.Command]]
    ) -> None:
        bot = self.context.bot
        embed: Embed = Embed(
            description=f"{Emoji.CHECKMARK} **Here are all my modules!**",
            color=Colors.DEFAULT,
        )
        embed.set_author(
            name=bot.user.name,
            icon_url=Links.BOT_AVATAR_URL,
            url=Links.BOT_DOCUMENTATION_URL,
        )
        embed.set_thumbnail(url=Links.BOT_AVATAR_URL)
        embed.set_footer(
            text=f"Requested By {self.context.author.name}",
            icon_url=self.context.author.avatar.url,
        )
        usable_commands = await self.filter_commands(
            self.context.bot.commands, sort=True
        )
        usable_cogs = {
            command.cog for command in usable_commands if command.cog is not None
        }
        for cog in usable_cogs:
            embed.add_field(
                name=f"{cog.emoji} {cog.qualified_name}",
                value=f"`{self.context.clean_prefix}help {cog.qualified_name}`",
            )
        await self.dispatch_help(embed)

    async def send_command_help(self, command: commands.Command) -> None:
        embed: Embed = Embed(title=f"Help For: `{command.name}`", color=Colors.DEFAULT)
        embed.add_field(
            name=f"{Emoji.QUESTION} What does this command do?",
            value=command.description
            if command.description is not None
            else "No Description",
            inline=False,
        )
        embed.add_field(
            name="Usage",
            value=f"`{self.get_command_signature(command)}`",
            inline=False,
        )

        examples = command.extras["Examples"]

        if examples:
            has_examples: Literal[True] = True
        else:
            has_examples: Literal[True] = False

        if command.extras["Notes"]:
            has_notes: Literal[True] = True
        else:
            has_notes: Literal[True] = False

        if has_examples:
            embed.add_field(name="Examples", value=f"`{examples}`", inline=False)

        if has_notes:
            embed.add_field(name="Extra Notes", value=command.extras["Notes"])

        has_cooldown: bool = command._buckets._cooldown is not None

        if has_cooldown:
            delta: timedelta = datetime.timedelta(
                seconds=command._buckets._cooldown.per
            )
            cooldown: str = humanize.precisedelta(delta, format="%0.0f")
            embed.add_field(name="Cooldown", value=f"`{cooldown}`", inline=False)
        else:
            embed.add_field(name="Cooldown", value=f"`0` (No Cooldown)", inline=False)

        await self.dispatch_help(embed)

    async def send_group_help(self, group: commands.Group) -> None:
        embed: Embed = Embed(
            title=f"Help For Command: `{group.name}`", color=Colors.DEFAULT
        )
        embed.add_field(
            name=f"{Emoji.QUESTION} What does this command do?",
            value=group.description
            if group.description is not None
            else "No Description",
            inline=False,
        )
        embed.add_field(
            name="Usage",
            value=f"`{self.get_command_signature(group)}`",
            inline=False,
        )

        subcommand_help: List[str] = [
            f"**`{self.get_command_signature(command)}`**\n{command.description}"
            for command in group.commands
        ]
        newline: Literal["\n"] = "\n"
        embed.add_field(
            name="Related commands",
            value=f"\n{newline.join(subcommand_help)}",
            inline=False,
        )
        await self.dispatch_help(embed)

    async def send_cog_help(self, cog: CustomCog) -> None:
        embed: Embed = Embed(
            title=f"Help For Module: {cog.emoji} `{cog.qualified_name}`",
            color=Colors.DEFAULT,
        )
        embed.add_field(
            name=f"{Emoji.QUESTION} What does this category do?",
            value=cog.description if cog.description is not None else "No Description",
            inline=False,
        )
        for command in cog.walk_commands():
            if command.parent is None:
                embed.add_field(
                    name=f"`{self.context.clean_prefix}{command.name}`",
                    value=command.description
                    if command.description is not None
                    else "No Command Description",
                    inline=False,
                )
        await self.dispatch_help(embed)
