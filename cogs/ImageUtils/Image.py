"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

from io import BytesIO
from typing import Optional

import aiohttp
import discord
from asyncdagpi import Client as DagpiClient
from asyncdagpi import ImageFeatures
from discord.ext import commands

from config.ext.parser import config
from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log


class ImageUtils(
    Cog,
    name="Image Utils",
    description="Funny Image Utilities",
    emoji=Emoji.IMAGE,
):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.dagpi_client = DagpiClient(
            config["DAGPI_API_KEY"], session=self.bot.session
        )

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    async def get_member_avatar(self, member: discord.Member):
        member_avatar_url = member.avatar.replace(format="png", static_format="png").url
        return await member_avatar_url

    async def generate_file(self, image: BytesIO, member: discord.Member, name: str):
        file = discord.File(fp=image, filename=f"{member.name}-{name}.gif")
        return file

    @commands.command(
        name="triggered",
        description="Return Triggered Image Of Someones Avatar",
        extras={"Examples": "triggered (works with no mention)\ntriggered @Member"},
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
        extras={"Examples": "wanted @Member\nwanted (works with no mention)"},
    )
    async def wanted(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.dagpi_client.image_process(
                ImageFeatures.wanted(), await self.get_member_avatar(member).url
            )

            file = discord.File(fp=image.image, filename=f"wanted.{image.format}")

            await ctx.send(file=file)

    @commands.command(
        name="bonk",
        description="Return Bonk Image Of Someones Avatar",
        extras={"Examples": "bonk @Member\nbonk"},
    )
    async def bonk(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.bonks(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "bonks")

            await ctx.send(file=file)

    @commands.command(
        name="patpat",
        description=f"Return Pat Image Of Someones Avatar",
        extras={"Examples": "patpat @Member\npatpat"},
    )
    async def patpat(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.patpat(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "patpat")

            await ctx.send(file=file)

    @commands.command(
        name="burn",
        description=f"Return Burned Image Of Someones Avatar",
        extras={"Examples": "burn @Member\nburn"},
    )
    async def burn(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.burn(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "burn")

            await ctx.send(file=file)

    @commands.command(
        name="glitch",
        description=f"Return Glitched Image Of Someones Avatar",
        extras={"Examples": "glitch @Member\nglitch"},
    )
    async def glitch(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.glitch(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "glitch")

            await ctx.send(file=file)

    @commands.command(
        name="boil",
        description=f"Return Boiled Image Of Someones Avatar",
        extras={"Examples": "boil @Member\nboil"},
    )
    async def boil(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.boil(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "boil")

            await ctx.send(file=file)

    @commands.command(
        name="earthquake",
        description=f"Return Earthquake Image Of Someones Avatar",
        extras={"Examples": "earthquake @Member\nearthquake"},
    )
    async def earthquake(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.earthquake(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "earthquake")

            await ctx.send(file=file)

    @commands.command(
        name="hearts",
        description=f"Return hearts Image Of Someones Avatar",
        extras={"Examples": "hearts @Member\nhearts"},
    )
    async def hearts(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.hearts(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "hearts")

            await ctx.send(file=file)

    @commands.command(
        name="shock",
        description=f"Return Shocked Image Of Someones Avatar",
        extras={"Examples": "shock @Member\nshock"},
    )
    async def shock(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.shock(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "shock")

            await ctx.send(file=file)

    @commands.command(
        name="abstract",
        description=f"Return Abstracted Image Of Someones Avatar",
        extras={"Examples": "abstract @Member\nabstract"},
    )
    async def abstract(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.abstract(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "abstract")

            await ctx.send(file=file)

    @commands.command(
        name="infinity",
        description=f"Return Infinity Image Of Someones Avatar",
        extras={"Examples": "infinity @Member\ninfinity"},
    )
    async def infinity(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.infinity(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "infinity")

            await ctx.send(file=file)

    @commands.command(
        name="bomb",
        description=f"Return Bomb Image Of Someones Avatar",
        extras={"Examples": "bomb @Member\nbomb"},
    )
    async def bomb(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.bomb(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "bomb")

            await ctx.send(file=file)

    @commands.command(
        name="explicit",
        description=f"Return Explicit Image Of Someones Avatar",
        extras={"Examples": "explicit @Member\nexplicit"},
    )
    async def explicit(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.explicit(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "explicit")

            await ctx.send(file=file)

    @commands.command(
        name="blur",
        description=f"Return Blurred Image Of Someones Avatar",
        extras={"Examples": "blur @Member\nblur"},
    )
    async def blur(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.blur(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "blur")

            await ctx.send(file=file)

    @commands.command(
        name="lamp",
        description=f"Return Lamp Image Of Someones Avatar",
        extras={"Examples": "lamp @Member\nlamp"},
    )
    async def lamp(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.lamp(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "lamp")

            await ctx.send(file=file)

    @commands.command(
        name="rain",
        description=f"Return Rain Image Of Someones Avatar",
        extras={"Examples": "rain @Member\nrain"},
    )
    async def rain(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.rain(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "rain")

            await ctx.send(file=file)

    @commands.command(
        name="canny",
        description=f"Return Canny Image Of Someones Avatar",
        extras={"Examples": "canny @Member\ncanny"},
    )
    async def canny(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.canny(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "canny")

            await ctx.send(file=file)

    @commands.command(
        name="cartoon",
        description=f"Return Cartoon Image Of Someones Avatar",
        extras={"Examples": "cartoon @Member\ncartoon"},
    )
    async def cartoon(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.cartoon(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "cartoon")

            await ctx.send(file=file)

    @commands.command(
        name="layers",
        description=f"Return Layered Image Of Someones Avatar",
        extras={"Examples": "layers @Member\nlayers"},
    )
    async def layers(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.layers(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "layers")

            await ctx.send(file=file)

    @commands.command(
        name="radiate",
        description=f"Return Radiated Image Of Someones Avatar",
        extras={"Examples": "radiate @Member\nradiate"},
    )
    async def radiate(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.radiate(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "radiate")

            await ctx.send(file=file)

    @commands.command(
        name="shoot",
        description=f"Return Shoot Image Of Someones Avatar",
        extras={"Examples": "shoot @Member\nshoot"},
    )
    async def shoot(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.shoot(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "shoot")

            await ctx.send(file=file)

    @commands.command(
        name="tv",
        description=f"Return TV Image Of Someones Avatar",
        extras={"Examples": "tv @Member\ntv"},
    )
    async def tv(self, ctx: commands.Context, member: Optional[discord.Member]) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.tv(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "tv")

            await ctx.send(file=file)

    @commands.command(
        name="shear",
        description=f"Return sheared Image Of Someones Avatar",
        extras={"Examples": "shear @Member\nshear"},
    )
    async def shear(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.shear(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "shear")

            await ctx.send(file=file)

    @commands.command(
        name="magnify",
        description=f"Return magnify Image Of Someones Avatar",
        extras={"Examples": "magnify @Member\nmagnify"},
    )
    async def magnify(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.magnify(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "magnify")

            await ctx.send(file=file)

    @commands.command(
        name="print",
        description=f"Return print Image Of Someones Avatar",
        extras={"Examples": "print @Member\nprint"},
    )
    async def print(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.print(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "print")

            await ctx.send(file=file)

    @commands.command(
        name="matrix",
        description=f"Return matrix Image Of Someones Avatar",
        extras={"Examples": "matrix @Member\nmatrix"},
    )
    async def matrix(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.matrix(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "matrix")

            await ctx.send(file=file)

    @commands.command(
        name="sensitive",
        description=f"Return sensitive Image Of Someones Avatar",
        extras={"Examples": "sensitive @Member\nsensitive"},
    )
    async def sensitive(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.sensitive(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "sensitive")

            await ctx.send(file=file)

    @commands.command(
        name="gallery",
        description=f"Return gallery Image Of Someones Avatar",
        extras={"Examples": "gallery @Member\ngallery"},
    )
    async def gallery(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.gallery(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "gallery")

            await ctx.send(file=file)

    @commands.command(
        name="paparazzi",
        description=f"Return paparazzi Image Of Someones Avatar",
        extras={"Examples": "paparazzi @Member\npaparazzi"},
    )
    async def paparazzi(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.paparazzi(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "paparazzi")

            await ctx.send(file=file)

    @commands.command(
        name="balls",
        description=f"Return balls Image Of Someones Avatar",
        extras={"Examples": "balls @Member\nballs"},
    )
    async def balls(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.balls(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "balls")

            await ctx.send(file=file)

    @commands.command(
        name="equation",
        description=f"Return equation Image Of Someones Avatar",
        extras={"Examples": "equation @Member\nequation"},
    )
    async def equation(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.equation(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "equation")

            await ctx.send(file=file)

    @commands.command(
        name="half_invert",
        description=f"Return half_invert Image Of Someones Avatar",
        extras={"Examples": "half_invert @Member\nhalf_invert"},
    )
    async def half_invert(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.half_invert(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "half_invert")

            await ctx.send(file=file)

    @commands.command(
        name="roll",
        description=f"Return roll Image Of Someones Avatar",
        extras={"Examples": "roll @Member\nroll"},
    )
    async def roll(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.roll(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "roll")

            await ctx.send(file=file)

    @commands.command(
        name="clock",
        description=f"Return clock Image Of Someones Avatar",
        extras={"Examples": "clock @Member\nclock"},
    )
    async def clock(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.clock(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "clock")

            await ctx.send(file=file)

    @commands.command(
        name="optics",
        description=f"Return optics Image Of Someones Avatar",
        extras={"Examples": "optics @Member\noptics"},
    )
    async def optics(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.optics(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "optics")

            await ctx.send(file=file)

    @commands.command(
        name="warp",
        description=f"Return warp Image Of Someones Avatar",
        extras={"Examples": "warp @Member\nwarp"},
    )
    async def warp(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.warp(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "warp")

            await ctx.send(file=file)

    @commands.command(
        name="youtube",
        description=f"Return youtube Image Of Someones Avatar",
        extras={"Examples": "youtube @Member\nyoutube"},
    )
    async def youtube(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.youtube(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "youtube")

            await ctx.send(file=file)

    @commands.command(
        name="scrapbook",
        description=f"Return scrapbook Image Of Someones Avatar",
        extras={"Examples": "scrapbook @Member\nscrapbook"},
    )
    async def scrapbook(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.scrapbook(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "scrapbook")

            await ctx.send(file=file)

    @commands.command(
        nme="sob",
        description="Return sobbing image of someones avatar",
        extras={"Examples": "sob @Member\nsob"},
    )
    async def sob(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if not member:
            member = ctx.author

        async with ctx.channel.typing():
            image = await self.bot.jeyyapi_client.sob(
                await self.get_member_avatar(member)
            )

            file = await self.generate_file(image, member, "sob")

            await ctx.send(file=file)


def setup(bot):
    bot.add_cog(ImageUtils(bot))
