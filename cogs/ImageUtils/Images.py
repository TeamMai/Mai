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

import discord
import aiohttp

from typing import Optional
from discord.ext import commands

from jeyyapi import JeyyAPIClient
from asyncdagpi import Client as DagpiClient
from asyncdagpi import ImageFeatures

from helpers.constants import *
from helpers.logging import log
from helpers.custommeta import CustomCog as Cog

from config.ext.parser import config


class ImageUtils(
    Cog,
    name="Image Utils",
    description="Funny Image Utilities",
    emoji=Emoji.IMAGE,
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.jeyyapi_client = JeyyAPIClient(session=self.bot.session)
        self.dagpi_client = DagpiClient(
            config["DAGPI_API_KEY"], session=self.bot.session
        )

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.command(
        name="triggered",
        description="Return Triggered Image Of Someones Avatar",
        brief="triggered (works with no mention)\ntriggered @Member",
    )
    async def triggered(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                avatar = member.avatar.with_static_format("png")
                async with session.get(
                    f'https://some-random-api.ml/canvas/triggered?avatar={avatar}&key={config["SOME_RANDOM_API_KEY"]}'
                ) as resp:
                    await ctx.send(resp.url)

    @commands.command(
        name="wanted",
        description="Return Wanted Image Of Someones Avatar",
        brief="wanted @Member\nwanted (works with no mention)",
    )
    async def wanted(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            )

            image = await self.dagpi_client.image_process(
                ImageFeatures.wanted(), member_avatar_url.url
            )

            file = discord.File(
                fp=image.image, filename=f"wanted.{image.format}"
            )

            await ctx.send(file=file)

    @commands.command(
        name="bonk",
        description="Return Bonk Image Of Someones Avatar",
        brief="bonk @Member\nbonk",
    )
    async def bonk(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.bonks(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-bonks.gif")

            await ctx.send(file=file)

    @commands.command(
        name="patpat",
        description=f"Return Pat Image Of Someones Avatar",
        brief="patpat @Member\npatpat",
    )
    async def patpat(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.patpat(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-patpat.gif")

            await ctx.send(file=file)

    @commands.command(
        name="burn",
        description=f"Return Burned Image Of Someones Avatar",
        brief="burn @Member\nburn",
    )
    async def burn(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.burn(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-burn.gif")

            await ctx.send(file=file)

    @commands.command(
        name="glitch",
        description=f"Return Glitched Image Of Someones Avatar",
        brief="glitch @Member\nglitch",
    )
    async def glitch(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.glitch(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-glitch.gif")

            await ctx.send(file=file)

    @commands.command(
        name="boil",
        description=f"Return Boiled Image Of Someones Avatar",
        brief="boil @Member\nboil",
    )
    async def boil(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.boil(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-___.gif")

            await ctx.send(file=file)

    @commands.command(
        name="earthquake",
        description=f"Return Earthquake Image Of Someones Avatar",
        brief="earthquake @Member\nearthquake",
    )
    async def earthquake(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.earthquake(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-___.gif")

            await ctx.send(file=file)

    @commands.command(
        name="hearts",
        description=f"Return hearts Image Of Someones Avatar",
        brief="hearts @Member\nhearts",
    )
    async def hearts(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.hearts(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-hearts.gif")

            await ctx.send(file=file)

    @commands.command(
        name="shock",
        description=f"Return Shocked Image Of Someones Avatar",
        brief="shock @Member\nshock",
    )
    async def shock(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.shock(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-shock.gif")

            await ctx.send(file=file)

    @commands.command(
        name="abstract",
        description=f"Return Abstracted Image Of Someones Avatar",
        brief="abstract @Member\nabstract",
    )
    async def abstract(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.abstract(member_avatar_url)

            file = discord.File(
                fp=image, filename=f"{member.name}-abstract.gif"
            )

            await ctx.send(file=file)

    @commands.command(
        name="infinity",
        description=f"Return Infinity Image Of Someones Avatar",
        brief="infinity @Member\ninfinity",
    )
    async def infinity(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.infinity(member_avatar_url)

            file = discord.File(
                fp=image, filename=f"{member.name}-infinity.gif"
            )

            await ctx.send(file=file)

    @commands.command(
        name="bomb",
        description=f"Return Bomb Image Of Someones Avatar",
        brief="bomb @Member\nbomb",
    )
    async def bomb(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.bomb(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-bomb.gif")

            await ctx.send(file=file)

    @commands.command(
        name="explicit",
        description=f"Return Explicit Image Of Someones Avatar",
        brief="explicit @Member\nexplicit",
    )
    async def explicit(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.explicit(member_avatar_url)

            file = discord.File(
                fp=image, filename=f"{member.name}-explicit.gif"
            )

        await ctx.send(file=file)

    @commands.command(
        name="blur",
        description=f"Return Blurred Image Of Someones Avatar",
        brief="blur @Member\nblur",
    )
    async def blur(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.blur(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-blur.gif")

            await ctx.send(file=file)

    @commands.command(
        name="lamp",
        description=f"Return Lamp Image Of Someones Avatar",
        brief="lamp @Member\nlamp",
    )
    async def lamp(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.lamp(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-lamp.gif")

            await ctx.send(file=file)

    @commands.command(
        name="rain",
        description=f"Return Rain Image Of Someones Avatar",
        brief="rain @Member\nrain",
    )
    async def rain(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.rain(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-rain.gif")

            await ctx.send(file=file)

    @commands.command(
        name="canny",
        description=f"Return Canny Image Of Someones Avatar",
        brief="canny @Member\ncanny",
    )
    async def canny(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.canny(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-canny.gif")

            await ctx.send(file=file)

    @commands.command(
        name="cartoon",
        description=f"Return Cartoon Image Of Someones Avatar",
        brief="cartoon @Member\ncartoon",
    )
    async def cartoon(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.cartoon(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-cartoon.gif")

            await ctx.send(file=file)

    @commands.command(
        name="layers",
        description=f"Return Layered Image Of Someones Avatar",
        brief="layers @Member\nlayers",
    )
    async def layers(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.layers(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-layers.gif")

            await ctx.send(file=file)

    @commands.command(
        name="radiate",
        description=f"Return Radiated Image Of Someones Avatar",
        brief="radiate @Member\nradiate",
    )
    async def radiate(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.radiate(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-radiate.gif")

            await ctx.send(file=file)

    @commands.command(
        name="shoot",
        description=f"Return Shoot Image Of Someones Avatar",
        brief="shoot @Member\nshoot",
    )
    async def shoot(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.shoot(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-shoot.gif")

            await ctx.send(file=file)

    @commands.command(
        name="tv",
        description=f"Return TV Image Of Someones Avatar",
        brief="tv @Member\ntv",
    )
    async def tv(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.tv(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-tv.gif")

            await ctx.send(file=file)

    @commands.command(
        name="shear",
        description=f"Return sheared Image Of Someones Avatar",
        brief="shear @Member\nshear",
    )
    async def shear(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.shear(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-shear.gif")

            await ctx.send(file=file)

    @commands.command(
        name="magnify",
        description=f"Return magnify Image Of Someones Avatar",
        brief="magnify @Member\nmagnify",
    )
    async def magnify(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.magnify(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-magnify.gif")

            await ctx.send(file=file)

    @commands.command(
        name="print",
        description=f"Return print Image Of Someones Avatar",
        brief="print @Member\nprint",
    )
    async def print(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.print(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-print.gif")

            await ctx.send(file=file)

    @commands.command(
        name="matrix",
        description=f"Return matrix Image Of Someones Avatar",
        brief="matrix @Member\nmatrix",
    )
    async def matrix(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.matrix(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-matrix.gif")

            await ctx.send(file=file)

    @commands.command(
        name="sensitive",
        description=f"Return sensitive Image Of Someones Avatar",
        brief="sensitive @Member\nsensitive",
    )
    async def sensitive(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.sensitive(member_avatar_url)

            file = discord.File(
                fp=image, filename=f"{member.name}-sensitive.gif"
            )

            await ctx.send(file=file)

    @commands.command(
        name="gallery",
        description=f"Return gallery Image Of Someones Avatar",
        brief="gallery @Member\ngallery",
    )
    async def gallery(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.gallery(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-gallery.gif")

            await ctx.send(file=file)

    @commands.command(
        name="paparazzi",
        description=f"Return paparazzi Image Of Someones Avatar",
        brief="paparazzi @Member\npaparazzi",
    )
    async def paparazzi(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.paparazzi(member_avatar_url)

            file = discord.File(
                fp=image, filename=f"{member.name}-paparazzi.gif"
            )

            await ctx.send(file=file)

    @commands.command(
        name="balls",
        description=f"Return balls Image Of Someones Avatar",
        brief="balls @Member\nballs",
    )
    async def balls(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.balls(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-balls.gif")

            await ctx.send(file=file)

    @commands.command(
        name="equation",
        description=f"Return equation Image Of Someones Avatar",
        brief="equation @Member\nequation",
    )
    async def equation(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.equation(member_avatar_url)

            file = discord.File(
                fp=image, filename=f"{member.name}-equation.gif"
            )

            await ctx.send(file=file)

    @commands.command(
        name="half_invert",
        description=f"Return half_invert Image Of Someones Avatar",
        brief="half_invert @Member\nhalf_invert",
    )
    async def half_invert(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.half_invert(member_avatar_url)

            file = discord.File(
                fp=image, filename=f"{member.name}-half_invert.gif"
            )

            await ctx.send(file=file)

    @commands.command(
        name="roll",
        description=f"Return roll Image Of Someones Avatar",
        brief="roll @Member\nroll",
    )
    async def roll(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.roll(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-roll.gif")

            await ctx.send(file=file)

    @commands.command(
        name="clock",
        description=f"Return clock Image Of Someones Avatar",
        brief="clock @Member\nclock",
    )
    async def clock(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.clock(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-clock.gif")

            await ctx.send(file=file)

    @commands.command(
        name="optics",
        description=f"Return optics Image Of Someones Avatar",
        brief="optics @Member\noptics",
    )
    async def optics(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.optics(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-optics.gif")

            await ctx.send(file=file)

    @commands.command(
        name="warp",
        description=f"Return warp Image Of Someones Avatar",
        brief="warp @Member\nwarp",
    )
    async def warp(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.warp(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-___.gif")

            await ctx.send(file=file)

    @commands.command(
        name="youtube",
        description=f"Return youtube Image Of Someones Avatar",
        brief="youtube @Member\nyoutube",
    )
    async def youtube(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.youtube(member_avatar_url)

            file = discord.File(fp=image, filename=f"{member.name}-youtube.gif")

            await ctx.send(file=file)

    @commands.command(
        name="scrapbook",
        description=f"Return scrapbook Image Of Someones Avatar",
        brief="scrapbook @Member\nscrapbook",
    )
    async def scrapbook(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            member_avatar_url = member.avatar.replace(
                format="png", static_format="png"
            ).url

            image = await self.jeyyapi_client.scrapbook(member_avatar_url)

            file = discord.File(
                fp=image, filename=f"{member.name}-scrapbook.gif"
            )

            await ctx.send(file=file)


def setup(bot):
    bot.add_cog(ImageUtils(bot))
