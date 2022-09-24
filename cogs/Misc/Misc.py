"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import io
import platform
import time
from datetime import datetime
from typing import Final, Optional

import aiohttp
import discord
import humanize
import psutil
from discord.ext import commands
from discord.ext.commands import Bot, BucketType
from sympy.core.symbol import var
from sympy.parsing.sympy_parser import (
    implicit_multiplication,
    parse_expr,
    standard_transformations,
)

from config.ext.parser import config
from db.models import Guild
from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log
from helpers.types import *
from views.info import Invite, Source, SupportServer


class Miscellaneous(
    Cog,
    name="Misc",
    description="Miscellaneous commands about Mai",
    emoji=Emoji.QUESTION,
):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot
        self.SS_FORMAT: Final[str] = "jpeg"

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.command(
        name="invite",
        description="Get An Invite To The Bot",
        extras={"Examples": "invite"},
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def invite(self, ctx: commands.Context) -> None:
        await ctx.send(f"Here is your link {ctx.author.mention}!", view=Invite())

    @commands.command(
        name="support",
        description="Get An Invite To The Bot Support Server",
        extras={"Examples": "invite"},
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def support(self, ctx: commands.Context) -> None:
        await ctx.send("Join The Support Server!", view=SupportServer())

    @commands.command(
        name="source",
        aliases=["src"],
        description="Get An Link To The Bot's Source Code",
        extras={"Examples": "source"},
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def source(self, ctx: commands.Context) -> None:
        await ctx.send("Here is your link", view=Source())

    @commands.command(name="ping", description="pong", extras={"Examples": "ping"})
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.trigger_typing()
        before = time.monotonic()
        loading_embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"{Emoji.LOADING_CIRCLE} Pinging...",
        )
        message = await ctx.send(embed=loading_embed)

        ping = (time.monotonic() - before) * 1000
        pEmbed = discord.Embed(title="Stats:", color=Colors.DEFAULT)
        pEmbed.add_field(name=f"{Emoji.MAI} Latency", value=f"{int(ping)}ms")
        pEmbed.add_field(
            name=f"{Emoji.DISCORD} API",
            value=f"{round(self.bot.latency * 1000)}ms",
        )

        db_time_start = time.time()
        guild = await Guild.get(discord_id=ctx.guild.id)
        db_time_end = time.time()
        db_time = db_time_end - db_time_start
        pEmbed.add_field(
            name=f"{Emoji.POSTGRESQL} Database",
            value=f"{round(db_time * 1000)}ms",
        )

        redis_time_start = time.time()
        from db.models import redis

        redis.ping()
        redis_time_end = time.time()
        redis_time = redis_time_end - redis_time_start
        pEmbed.add_field(
            name=f"{Emoji.REDIS} Redis", value=f"{round(redis_time * 1000)}ms"
        )

        pEmbed.set_thumbnail(url=Links.BOT_AVATAR_URL)
        pEmbed.set_footer(text=Mai.DEVELOPER_FOOTER, icon_url=Links.BOT_AVATAR_URL)
        await message.edit(content=None, embed=pEmbed)
        await message.add_reaction(Emoji.WHITE_CHECKMARK)

    @commands.command(
        name="uptime", description="Get Mai's Uptime", extras={"Examples": "uptime"}
    )
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.guild_only()
    async def uptime(self, ctx: commands.Context) -> None:
        await ctx.trigger_typing()
        now = datetime.utcnow()

        start_time = self.bot.uptime

        uptime = start_time - now

        humanized_uptime = humanize.precisedelta(
            uptime.total_seconds(), minimum_unit="milliseconds", format="%0.2f"
        )

        embed = discord.Embed(
            title="Bot Uptime",
            color=Colors.DEFAULT,
            description=f"{Char.ARROW} {humanized_uptime}",
        )

        await ctx.send(embed=embed)

    @commands.command(
        name="info",
        aliases=["stats"],
        description="Get bot stats",
        extras={"Examples": "stats"},
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def stats(self, ctx: commands.Context) -> None:

        await ctx.trigger_typing()

        loading_embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"{Emoji.LOADING_CIRCLE} Fetching Stats...",
        )
        message = await ctx.send(embed=loading_embed)

        embed = discord.Embed(title="Mai Information", color=Colors.DEFAULT)

        embed.set_thumbnail(url=Links.BOT_AVATAR_URL)

        ghoul = ctx.guild.get_member(Mai.GHOUL_DISCORD_ID)
        nerd = ctx.guild.get_member(Mai.NERD_DISCORD_ID)

        if ctx.guild.id == Mai.SUPPORT_SERVER_ID:
            developers = f"Developers: {ghoul.mention}, {nerd.mention}"
        else:
            developers = f"Developers: `ghoul#0002`, `Nerd#4271`"

        embed.add_field(
            name=f"{Emoji.OWNER} Developers",
            value=f"{developers}",
            inline=False,
        )

        servers = f"{Emoji.INFORMATION} Servers: `{len(self.bot.guilds)}`"
        users = f"{Emoji.MENTION} Users: `{len(self.bot.users)}`"

        voice_channel_list = [len(guild.voice_channels) for guild in self.bot.guilds]
        voice_channels = (
            f"{Emoji.VOICE_CHANNEL} Voice Channels: `{sum(voice_channel_list)}`"
        )

        text_channels_list = [len(guild.text_channels) for guild in self.bot.guilds]
        text_channels = f"{Emoji.CHANNEL} Text Channels: `{sum(text_channels_list)}`"

        stage_channel_list = [len(guild.stage_channels) for guild in self.bot.guilds]
        stage_channels = (
            f"{Emoji.STAGE_CHANNEL} Stage Channels: `{sum(stage_channel_list)}`"
        )

        commands = f"{Emoji.SLASH_COMMAND} Commands: `{len(self.bot.commands)}`"

        embed.add_field(
            name=f"{Emoji.STATS} Statistics",
            value=f"{servers}\n{users}\n{voice_channels}\n{text_channels}\n{stage_channels}\n{commands}",
            inline=False,
        )

        virtual_mem = psutil.virtual_memory()

        os = f"{Emoji.WINDOWS_10} OS: `Windows`"
        cpu = f"{Emoji.CPU} CPU: `{psutil.cpu_percent()}%`"
        ram = f"{Emoji.RAM} RAM: `{virtual_mem.percent}%`"

        embed.add_field(
            name=f"{Emoji.PC} PC", value=f"{os}\n{cpu}\n{ram}", inline=False
        )

        python = f"{Emoji.PYTHON} Python: `{platform.python_version()}`"
        pycord = f"{Emoji.PYCORD} Pycord: `{discord.__version__}`"
        mai_version = config["BOT_VERSION"]
        mai = f"{Emoji.MAI} Mai: `{mai_version}`"

        embed.add_field(
            name=f"{Emoji.STATS} Versions",
            value=f"{python}\n{pycord}\n{mai}",
            inline=False,
        )

        bot_invite = f"[Bot Invite]({Links.BOT_INVITE_URL})"
        source_code = f"[Source Code]({Links.BOT_SOURCE_CODE_URL})"
        support_server = f"[Support Server]({Links.SUPPORT_SERVER_INVITE})"
        documentation = f"[Documentation]({Links.BOT_DOCUMENTATION_URL})"
        embed.add_field(
            name=f"{Emoji.LINK} Links",
            value=f"{bot_invite}\n{support_server}\n{source_code}\n{documentation}",
            inline=False,
        )

        embed.set_footer(text=Mai.DEVELOPER_FOOTER, icon_url=ctx.author.avatar.url)

        await message.edit(content=None, embed=embed)

    @commands.command(
        name="math",
        description="Execute Math",
        extras={"Examples": "math 1 + 1\nmath 3p p=43"},
    )
    @commands.guild_only()
    async def math(
        self, ctx: commands.Context, expression: str, *, vars: Optional[str]
    ) -> None:
        await ctx.trigger_typing()

        loading_embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"{Emoji.LOADING_CIRCLE} Calculating...",
        )
        message = await ctx.send(embed=loading_embed)

        if vars is not None:
            declarations = vars.split(";")
            runtime_vars = dict()
            for declaration in declarations:
                lhs, rhs = tuple(declaration.split("="))
                runtime_vars.update({lhs: int(rhs)})
        else:
            runtime_vars = dict()

        result = parse_expr(
            expression,
            local_dict=runtime_vars,
            transformations=standard_transformations + (implicit_multiplication,),
        )
        embed = discord.Embed(
            title=f"Math Calculated {Emoji.BRAIN}",
            color=Colors.SUCCESS,
            timestamp=datetime.utcnow(),
        )
        embed.add_field(name="Expression", value=expression, inline=False)
        var_mappings = "\n".join(
            [f"{var} -> {val}" for var, val in runtime_vars.items()]
        )
        if var_mappings:
            embed.add_field(name="Runtime variables", value=var_mappings, inline=False)
        embed.add_field(name="Result", value=result, inline=False)
        await message.edit(content=None, embed=embed)

    @commands.command(
        name="avatar",
        description="Get Avatar of a User",
        aliases=["av"],
        extras={"Examples": "av"},
    )
    async def avatar(self, ctx: commands.Context, user: discord.Member = None):
        if not user:
            user = ctx.author

        embed = discord.Embed(
            description=f"[[Open In Browser]({user.avatar.url})]",
            colour=Colors.DEFAULT,
        )
        embed.set_author(name=user, url=user.avatar.url, icon_url=user.avatar.url)
        embed.set_image(url=user.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}")

        await ctx.send(embed=embed)

    @commands.command(
        name="banner",
        description="Get Banner of User",
        extras={"Examples": "banner @Member\nbanner"},
    )
    async def banner(self, ctx: commands.Context, user: discord.Member = None):
        if not user:
            user = ctx.author

        user = await self.bot.fetch_user(user.id)

        if not user.banner:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} {user.mention} has no banner!",
            )
            await ctx.send(embed=embed)
            return

        if user.banner.is_animated():
            gif = user.banner.with_format("gif").url
            embed = discord.Embed(
                description=f"[[Open In Browser]({gif})]", color=Colors.DEFAULT
            )
            embed.set_image(url=gif)
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=ctx.author.avatar.url,
            )
            await ctx.send(embed=embed)
        else:
            static = user.banner.with_format("png").url
            embed = discord.Embed(
                description=f"[[Open In Browser]({static})]",
                color=Colors.DEFAULT,
            )
            embed.set_image(url=static)
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=ctx.author.avatar.url,
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="serverbanner",
        description="Get Server Banner",
        extras={"Examples": "serverbanner"},
    )
    @commands.guild_only()
    async def serverbanner(self, ctx: commands.Context):
        if not ctx.guild.banner:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} `{ctx.guild.name}` has no banner!",
            )
            await ctx.send(embed=embed)
            return

        if ctx.guild.banner.is_animated():
            gif = ctx.guild.banner.with_format("gif").url
            embed = discord.Embed(
                description=f"[[Open In Browser]({gif})]", color=Colors.DEFAULT
            )
            embed.set_image(url=gif)
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=ctx.author.avatar.url,
            )
            await ctx.send(embed=embed)
        else:
            static = ctx.guild.banner.with_format("png").url
            embed = discord.Embed(
                description=f"[[Open In Browser]({static})]",
                color=Colors.DEFAULT,
            )
            embed.set_image(url=static)
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=ctx.author.avatar.url,
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="servericon",
        description="Get Server Icon",
        extras={"Examples": "servericon"},
    )
    @commands.guild_only()
    async def servericon(self, ctx: commands.Context):
        embed = discord.Embed(
            description=f"[[Open In Browser]({ctx.guild.icon.url})]",
            colour=Colors.DEFAULT,
        )
        embed.set_author(
            name=ctx.guild.name,
            url=ctx.guild.icon.url,
            icon_url=ctx.guild.icon.url,
        )
        embed.set_image(url=ctx.guild.icon.url)
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )

        await ctx.send(embed=embed)

    @commands.command(
        name="screenshot",
        aliases=["ss"],
        description="Take A Screenshot Of An Website",
        extras={
            "Notes": "**ONLY** `http://` and `https://` are supported.",
            "Examples": "screenshot https://google.com\nss https://google.com",
        },
    )
    @commands.guild_only()
    async def screenshot(
        self, ctx: commands.Context, url: str, delay: Optional[int]
    ) -> None:
        if delay is None:
            delay = 1

        embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"[`{url}`]({url})",
            timestamp=datetime.utcnow(),
        )
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)

        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                params = {
                    "access_key": config["API_FLASH_TOKEN"],
                    "url": url,
                    "format": self.SS_FORMAT,
                    "fresh": "true",
                    "quality": 100,
                    "delay": delay,
                    "response_type": "json",
                }
                async with session.get(
                    "https://api.apiflash.com/v1/urltoimage", params=params
                ) as response:

                    json = await response.json()
                    url = json["url"]

                    embed.set_image(url=url)
                    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
