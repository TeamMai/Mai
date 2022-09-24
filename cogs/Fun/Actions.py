"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import random
from typing import Optional

import aiohttp
import discord
import nekos
from discord.ext import commands
from discord.ext.commands import Bot, BucketType, Greedy

from config.ext.parser import config
from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log


class Actions(Cog, name="Actions", description="Fun Commands", emoji=Emoji.INFORMATION):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.kawaii_red_token = config["KAWAII_RED_API_TOKEN"]

    async def kawaii_request(self, target: str) -> str:
        MAIN_ENDPOINT = "https://kawaii.red/api/gif"
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{MAIN_ENDPOINT}/{target}/token={self.kawaii_red_token}&type=json/"
            ) as response:
                json = await response.json()
                return json["response"]

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.command(
        name="poptart",
        description="Throws A Poptart At Random Members",
        extras={"Examples": "poptart @Member1 @Member2"},
    )
    @commands.guild_only()
    async def poptart(
        self, ctx: commands.Context, target: Greedy[discord.Member]
    ) -> None:

        number_of_targets = len(target)
        speed_of_light = 299792458
        rand_percentage = random.random()
        percentage_of_speed = speed_of_light * rand_percentage
        if number_of_targets == 1:
            formatted_targets = target[0].mention
        elif number_of_targets == 2:
            formatted_targets = f"{target[0].mention} and {target[1].mention}"
        else:
            comma_separated = ", ".join(map(lambda m: m.mention, target[:-1]))
            final_element = f", and {target[-1].mention}"
            formatted_targets = f"{comma_separated}{final_element}"
        await ctx.send(
            f"{ctx.author.display_name} throws a poptart at {formatted_targets} with a mind numbing speed of "
            f"{int(percentage_of_speed)} m/s, that's {rand_percentage * 100:.2f}% the speed of light!"
        )

    @commands.command(
        name="hug",
        description="Hug Someone Or Yourself",
        extras={"Examples": "hug @Member1"},
    )
    @commands.guild_only()
    async def hug(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            embed = discord.Embed(
                description=f"{ctx.author.mention} got hugged!",
                color=Colors.SUCCESS,
            )
        else:
            embed = discord.Embed(
                description=f"{ctx.author.mention} hugged {member.mention}",
                color=Colors.SUCCESS,
            )
        embed.set_image(url=nekos.img("hug"))
        await ctx.send(embed=embed)

    @commands.command(
        name="pat",
        description="Pat Someone Or Yourself",
        extras={"Examples": "pat @Member1"},
    )
    @commands.guild_only()
    async def pat(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            embed = discord.Embed(
                description=f"{ctx.author.mention} got patted!",
                color=Colors.SUCCESS,
            )
        else:
            embed = discord.Embed(
                description=f"{ctx.author.mention} pats {member.mention}",
                color=Colors.SUCCESS,
            )
        embed.set_image(url=nekos.img("pat"))
        await ctx.send(embed=embed)

    @commands.command(
        name="kill",
        description="Kill Someone Or Yourself",
        extras={"Examples": "kill @Member1"},
    )
    @commands.guild_only()
    async def kill(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            embed = discord.Embed(
                description=f"{ctx.author.mention} is a murderer!",
                color=Colors.SUCCESS,
            )
        else:
            embed = discord.Embed(
                description=f"{ctx.author.mention} KILLED {member.mention}",
                color=Colors.SUCCESS,
            )
        embed.set_image(url=await self.kawaii_request("kill"))
        await ctx.send(embed=embed)

    @commands.command(
        name="slap",
        description="Slap Someone Or Yourself",
        extras={"Examples": "slap @Member1"},
    )
    @commands.guild_only()
    async def slap(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            embed = discord.Embed(
                description=f"{ctx.author.mention} slapped!",
                color=Colors.SUCCESS,
            )
        else:
            embed = discord.Embed(
                description=f"{ctx.author.mention} slapped {member.mention}",
                color=Colors.SUCCESS,
            )
        embed.set_image(url=nekos.img("slap"))
        await ctx.send(embed=embed)

    @commands.command(
        name="lick",
        description="Lick Someone Or Yourself",
        extras={"Examples": "lick @Member1"},
    )
    @commands.guild_only()
    async def lick(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            embed = discord.Embed(
                description=f"{ctx.author.mention} got licked.",
                color=Colors.SUCCESS,
            )
        else:
            embed = discord.Embed(
                description=f"{ctx.author.mention} licked {member.mention}",
                color=Colors.SUCCESS,
            )
        embed.set_image(url=await self.kawaii_request("lick"))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Actions(bot))
