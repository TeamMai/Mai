"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import os
import sys
import discord
import aiohttp
import watchgod
import inspect
import itertools
import traceback
import datetime


from glob import glob
from typing import Tuple


from discord import AllowedMentions, Intents
from discord.ext import commands, tasks
from discord.ext.commands import AutoShardedBot
from discord.flags import MemberCacheFlags
from discord.errors import (
    NoEntryPointError,
    ExtensionFailed,
    ExtensionNotLoaded,
    ExtensionNotFound,
    ExtensionAlreadyLoaded,
)

from pycord18n.extension import I18nExtension, _


from rich.traceback import install

from pypresence import AioPresence

from tortoise import Tortoise
from tortoise.exceptions import IntegrityError

from config.ext.parser import config

from db.models import Guild, OSU, ServerLogging
from db.tortoise.config import tortoise_config

from help_command import MaiHelpCommand

from locales.languages import (
    SPANISH,
    ENGLISH,
    FRENCH,
    GERMAN,
    JAPANESE,
    KOREAN,
    RUSSIAN,
    TURKISH,
)

from helpers.console import console
from helpers.constants import *
from helpers.logging import log

os.system("cls" if sys.platform == "win32" else "clear")


class Mai(AutoShardedBot):
    def __init__(
        self,
        development_mode: str = None,
        extensions_dir: str = "cogs",
        *args,
        **kwargs,
    ):

        self.extensions_dir = extensions_dir

        development_mode_passed = development_mode is not None

        if not development_mode_passed:
            raise ValueError(
                "__init__ expects development_mode to be provided, got None"
            )

        self.session = aiohttp.ClientSession()

        self.bot_owners = config["BOT_OWNERS"]

        self.RPC = AioPresence(config["DISCORD_ID"])

        self.development_mode = development_mode

        self.version = config["BOT_VERSION"]
        self.redis_path = config["REDIS_URI"]
        self.default_prefix = config["DEFAULT_PREFIX"]

        self.github = Links.BOT_SOURCE_CODE_URL
        self.support_server = Links.SUPPORT_SERVER_INVITE
        self.documentation = Links.BOT_DOCUMENTATION_URL
        self.invite_url = Links.BOT_INVITE_URL

        # -- Tuple of all activities the bot will display as a status
        self.activities = itertools.cycle(
            (
                discord.Activity(
                    type=discord.ActivityType.watching, name="-help"
                ),
                lambda: discord.Activity(
                    type=discord.ActivityType.listening,
                    name=f"{len(bot.commands)} Commands | {len(bot.users)} Users | {len(bot.guilds)} Servers",
                ),
            )
        )

        self.i18n = I18nExtension(
            [
                FRENCH,
                ENGLISH,
                SPANISH,
                JAPANESE,
                GERMAN,
                KOREAN,
                TURKISH,
                RUSSIAN,
            ],
            fallback="en",
        )

        self.uptime = datetime.datetime.utcnow()

        # -- Initalizing parent class

        # -- Intents
        intents = Intents.default()
        intents.members = True
        intents.typing = False
        intents.presences = True
        intents.message_content = True

        chunk_guilds_at_startup = False
        allowed_mentions = AllowedMentions(everyone=False, roles=False)
        stuff_to_cache = MemberCacheFlags.from_intents(intents)

        super().__init__(
            intents=intents,
            command_prefix=self.determine_prefix,
            case_insensitive=True,
            help_command=MaiHelpCommand(),
            allowed_mentions=allowed_mentions,
            member_cache_flags=stuff_to_cache,
            chunk_guilds_at_startup=chunk_guilds_at_startup,
            max_messages=1000,
            *args,
            **kwargs,
        )
        self.load_extensions()

    async def determine_prefix(
        self, bot: commands.Bot, message: discord.Message
    ) -> str:
        guild = message.guild
        if guild:
            guild_model, _ = await Guild.c_get_or_create_by_discord_id(guild.id)
            return commands.when_mentioned_or(guild_model.prefix)(bot, message)
        else:
            return commands.when_mentioned_or(self.default_prefix)(bot, message)

    async def get_locale(self, ctx: commands.Context) -> None:
        pass  # FIXME Overriding get_locale for pycordi18n but it's broken so just pass for now.

    def load_extensions(
        self, reraise_exceptions: bool = False
    ) -> Tuple[Tuple[str], Tuple[str]]:
        loaded_extensions = set()
        failed_extensions = set()
        for file in map(
            lambda file_path: file_path.replace(os.path.sep, ".")[:-3],
            glob(f"{self.extensions_dir}/**/*.py", recursive=True),
        ):
            try:
                self.load_extension(file)
                loaded_extensions.add(file)
                log.info(
                    f"[bright_green][EXTENSION][/bright_green] [blue3]{file} LOADED[/blue3]"
                )
            except Exception as e:
                failed_extensions.add(file)
                log.info(
                    f"[bright red][EXTENSION ERROR][/bright red] [blue3]FAILED TO LOAD COG {file}[/blue3]"
                )
                if not reraise_exceptions:
                    traceback.print_exception(type(e), e, e.__traceback__)
                else:
                    raise e
        result = (tuple(loaded_extensions), tuple(failed_extensions))
        return result

    def _start(self) -> None:
        self.run(config["DISCORD_TOKEN"], reconnect=True)

    @tasks.loop(seconds=15)
    async def rich_presence(self) -> None:
        rpc_enabled = config["RPC_ENABLED"]
        docker_enabled = config["USE_DOCKER"]
        if rpc_enabled == True and docker_enabled == False:
            await self.RPC.update(
                details=f"{len(self.guilds)} Guilds",
                state=f"{len(self.users)} Users",
                large_image=config["RPC_LARGE_IMAGE"],
                large_text=config["RPC_LARGE_TEXT"],
                small_image=config["RPC_SMALL_IMAGE"],
                small_text=config["RPC_SMALL_TEXT"],
                buttons=[
                    {"label": "Invite", "url": Links.BOT_INVITE_URL},
                    {
                        "label": "Support Server",
                        "url": Links.SUPPORT_SERVER_INVITE,
                    },
                ],
            )
            log.info(
                "[bright_green][RPC][/bright_green] [blue3]Rich Presence Updated.[/blue3]"
            )
        else:
            pass

    @tasks.loop(seconds=10)
    async def status(self) -> None:
        """Cycles through all status every 10 seconds"""
        new_activity = next(self.activities)
        # The commands one is callable so the command counts actually change
        if callable(new_activity):
            await self.change_presence(
                status=discord.Status.online, activity=new_activity()
            )
        else:
            await self.change_presence(
                status=discord.Status.online, activity=new_activity
            )

    @tasks.loop(seconds=1)
    async def cog_watcher_task(self) -> None:
        """Watches the cogs directory for changes and reloads files"""
        async for change in watchgod.awatch(
            self.extensions_dir, watcher_cls=watchgod.PythonWatcher
        ):
            for change_type, changed_file_path in change:
                try:
                    extension_name = changed_file_path.replace(
                        os.path.sep, "."
                    )[:-3]
                    if len(extension_name) > 36 and extension_name[-33] == ".":
                        continue
                    if change_type == watchgod.Change.modified:
                        try:
                            self.unload_extension(extension_name)
                        except ExtensionNotLoaded:
                            pass
                        finally:
                            self.load_extension(extension_name)
                            log.info(
                                f"[bright_green][EXTENSION][/bright_green] [blue3][AUTORELOADED] {extension_name}[/blue3]"
                            )
                    else:
                        self.unload_extension(extension_name)
                        log.info(
                            f"[bright_red][EXTENSION][/bright_red] [blue3][AUTOUNLOADED] {extension_name}[/blue3]"
                        )
                except (
                    ExtensionFailed,
                    NoEntryPointError,
                ) as e:
                    traceback.print_exception(type(e), e, e.__traceback__)

    @status.before_loop
    async def before_status(self) -> None:
        """Ensures the bot is fully ready before starting the task"""
        await self.wait_until_ready()

    async def on_ready(self) -> None:
        """Called when we have successfully connected to a gateway"""
        await Tortoise.init(tortoise_config.TORTOISE_CONFIG)
        await self.RPC.connect()
        # await self.i18n.init_bot(bot, self.get_locale(commands.Context)) 'cached_property' has no attribute 'id'. most likely due to how the pycordi18n uses pre_invoke, looking into it.

        console.print(
            "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]"
        )
        console.print(
            """[blue3]

    ███╗   ███╗ █████╗ ██╗    ██████╗  ██████╗ ████████╗      ██╗ ██████╗
    ████╗ ████║██╔══██╗██║    ██╔══██╗██╔═══██╗╚══██╔══╝     ██╔╝ ╚════██╗
    ██╔████╔██║███████║██║    ██████╔╝██║   ██║   ██║       ██╔╝   █████╔╝
    ██║╚██╔╝██║██╔══██║██║    ██╔══██╗██║   ██║   ██║       ╚██╗   ╚═══██╗
    ██║ ╚═╝ ██║██║  ██║██║    ██████╔╝╚██████╔╝   ██║        ╚██╗ ██████╔╝
    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝    ╚═════╝  ╚═════╝    ╚═╝         ╚═╝ ╚═════╝


[/blue3]""",
            justify="full",
        )

        console.print(
            f"[blue3]Signed into Discord as {self.user} (ID: {self.user.id}[/blue3])\n"
        )
        console.print(f"[blue3]Discord Version: {discord.__version__}[/blue3]")
        console.print(f"[blue3]Bot Version: {self.version}[/blue3]")
        console.print(f"[blue3]Redis Path: {self.redis_path}[/blue3]")
        console.print(f"[blue3]Default Prefix: {self.default_prefix}[/blue3]")
        console.print(
            f"[blue3]Development Version: {self.development_mode}[/blue3]"
        )
        console.print(
            "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]"
        )
        self.status.start()
        self.cog_watcher_task.start()
        self.rich_presence.start()


# Defining root level commands
bot = Mai(development_mode="development")

# -- Base Events
@bot.event
async def on_guild_join(guild: discord.Guild):
    try:
        guild = await Guild.create(
            discord_id=guild.id, language="en", prefix="-"
        )
        log.info(
            f"[blue3][GUILD] JOINED GUILD {guild.name}) (ID: {guild.id}) [/blue3]"
        )
    except IntegrityError:
        log.info(f"[blue3]{guild.name} ({guild.id}) Has Reinvited Mai.[/blue3]")


# -- Bot Checks


@bot.check
async def is_bot_on_maintenance_mode(ctx: commands.Context):

    maintenance_mode = config["MAINTENANCE_MODE"]
    bot_name = config["BOT_NAME"]

    if maintenance_mode and ctx.author.id not in bot.bot_owners:
        embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{Emoji.INFORMATION} {bot_name} Is Currently In Maintenance Mode, Try Again Later.",
        )
        await ctx.send(embed=embed)
        return False
    else:
        return True


@bot.check
async def is_guild_blacklisted(ctx: commands.Context):
    guild = await Guild.get(discord_id=ctx.guild.id)
    blacklisted = guild.is_bot_blacklisted
    bot_name = config["BOT_NAME"]

    if blacklisted and ctx.author.id not in bot.bot_owners:
        embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{ctx.author.mention}, {ctx.guild.name} Is blacklisted from using {bot_name} for breaking [{bot_name} TOS](https://soontobeourtoslink.com)",
        )
        await ctx.send(embed=embed)
        return False
    else:
        return True


# -- COG RELATED COMMANDS


@bot.command(aliases=["where", "find"])
@commands.is_owner()
async def which(ctx: commands.Context, *, command_name: str) -> None:
    """Finds the cog a command is part of"""
    command = bot.get_command(command_name)
    if command is None:
        embed = discord.Embed(
            description=f"{Emoji.ERROR} `{command_name}` **does not exist.**",
            color=Colors.ERROR,
        )
    else:
        inner_command = command.callback
        command_defined_on = inspect.getsourcelines(inner_command)[1]
        full_command_signature = f"`async def {inner_command.__name__}{inspect.signature(inner_command)}`"
        if type(command) is commands.Command and not command.parent:
            command_type = "`Standalone command`"
        elif type(command) is commands.Group:
            command_type = "`Command group`"
        else:
            command_type = f"Subcommand of `{command.parent.qualified_name}`"
        embed = discord.Embed(
            title="Target Acquired \U0001F3AF", color=Colors.SUCCESS
        )
        embed.add_field(
            name="Part of Extension",
            value=f"`{command.cog.qualified_name}`"
            if command.cog is not None
            else "`Root Module`",
            inline=False,
        )
        embed.add_field(name="Type of command", value=command_type)
        embed.add_field(
            name="Defined on line",
            value=f"`{command_defined_on}`",
            inline=False,
        )
        embed.add_field(
            name="Signature", value=full_command_signature, inline=False
        )
    await ctx.send(embed=embed)


@bot.command()
@commands.is_owner()
async def load(ctx: commands.Context, *, extentions: str) -> None:
    """Loads an extension, owners only"""

    if bot.development_mode != "development":
        embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{Emoji.ERROR} `bot.development_mode` set to `{bot.development_mode}`, commands such as `load`, `reload` and `unload` require `bot.development_mode` to be **development**",
        )
        await ctx.send(embed=embed)
        return

    if extentions is None:
        embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{Emoji.ERROR} `extention` argument missing",
        )
        await ctx.send(embed=embed)
        return

    loaded_extentions = []

    for extention in extentions.split():
        bot.load_extension(f"cogs.{extention}")
        loaded_extentions.append(extention)

    embed = discord.Embed(
        color=Colors.SUCCESS,
        description=f"{', '.join(extention)} Are Now Loaded!",
    )

    message = await ctx.send(embed=embed)

    await message.add_reaction(Emoji.CHECKMARK)


@load.error
async def load_error(
    ctx: commands.Context, error: commands.CommandError
) -> None:
    if isinstance(error, commands.NotOwner):
        embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{Emoji.ERROR} This Can Only Be Used By The Bot's Owners.",
        )
    elif isinstance(error, ExtensionAlreadyLoaded):
        embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{Emoji.ERROR} This Extension Is Already Loaded.",
        )
        await ctx.send(embed=embed)
    elif isinstance(error, ExtensionNotFound):
        embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{Emoji.ERROR} This Extension Does Not Exist.",
        )
        await ctx.send(embed=embed)
    else:
        traceback.print_exception(type(error), error, error.__traceback__)


@bot.command()
@commands.is_owner()
async def unload(ctx: commands.Context, *, extentions: str) -> None:
    """Unloads an extension, owners only"""
    if bot.development_mode != "development":
        embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{Emoji.ERROR} `bot.development_mode` set to `{bot.development_mode}`, commands such as `load`, `reload` and `unload` require `bot.development_mode` to be **development**",
        )
        await ctx.send(embed=embed)
        return

    if extentions is None:
        embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{Emoji.ERROR} `extention` argument missing",
        )
        await ctx.send(embed=embed)
        return

    loaded_extentions = []

    for extention in extentions.split():
        bot.unload_extension(f"cogs.{extention}")
        loaded_extentions.append(extention)

    embed = discord.Embed(
        color=Colors.SUCCESS,
        description=f"{', '.join(loaded_extentions)} Are Now UnLoaded!",
    )

    message = await ctx.send(embed=embed)

    await message.add_reaction(Emoji.CHECKMARK)


@unload.error
async def unload_error(
    ctx: commands.Context, error: commands.CommandError
) -> None:
    if isinstance(error, commands.NotOwner):
        embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{Emoji.ERROR} This Can Only Be Used By The Bot's Owners.",
        )
        await ctx.send(embed=embed)
    elif isinstance(error, ExtensionNotLoaded):
        embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{Emoji.ERROR} This Extension Is Not Loaded.",
        )
        await ctx.send(embed=embed)
    elif isinstance(error, ExtensionNotFound):
        embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{Emoji.ERROR} This Extension Does Not Exist.",
        )
        await ctx.send(embed=embed)
    else:
        traceback.print_exception(type(error), error, error.__traceback__)


@bot.command()
@commands.is_owner()
async def cogs(ctx: commands.Context) -> None:
    cogs = []

    for cog in bot.cogs:
        cogs.append(f"`{cog}`")

    cogs_str = ", ".join(cogs)
    embed = discord.Embed(
        title=f"All Cogs", description=cogs_str, colour=Colors.DEFAULT
    )
    await ctx.send(embed=embed)


@cogs.error
async def cogs_error(
    ctx: commands.Context, error: commands.CommandError
) -> None:
    if isinstance(error, commands.NotOwner):
        embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{Emoji.ERROR} This Can Only Be Used By The Bot's Owners.",
        )
        await ctx.send(embed=embed)
    else:
        traceback.print_exception(type(error), error, error.__traceback__)


@bot.command()
@commands.is_owner()
async def reload(ctx: commands.Context, *, extension: str) -> None:
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    embed = discord.Embed(
        color=Colors.SUCCESS,
        description=f"{Emoji.CHECKMARK} Successfully Reloaded {extension}",
    )
    await ctx.send(embed=embed)


@reload.error
async def reload_error(
    ctx: commands.Context, error: commands.CommandError
) -> None:
    if isinstance(error, commands.NotOwner):
        embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{Emoji.ERROR} This Can Only Be Used By The Bot's Owners.",
        )
    elif isinstance(error, ExtensionNotLoaded):
        embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{Emoji.ERROR} This Extension Is Not Loaded.",
        )
        await ctx.send(embed=embed)
    elif isinstance(error, ExtensionNotFound):
        embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{Emoji.ERROR} This Extension Does Not Exist.",
        )
        await ctx.send(embed=embed)
    else:
        traceback.print_exception(type(error), error, error.__traceback__)


if __name__ == "__main__":
    # Makes sure the bot only runs if this is run as main file
    try:
        bot._start()
        install(show_locals=True)
    except (KeyboardInterrupt):
        log.error("[red]Bot Start Interrupted By User.[/red]")
