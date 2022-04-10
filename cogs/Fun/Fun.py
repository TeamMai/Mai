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
import aiohttp

from discord.ext import commands

from typing import Optional, Union

from helpers.constants import *
from helpers.logging import log
from helpers.custommeta import CustomCog as Cog

from config.ext.parser import config


class Fun(Cog, name="Fun", description="Fun Commands", emoji=Emoji.INFORMATION):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.HTTP_ERROR_VALID_RANGES = (
            (100, 102),
            (200, 208),
            (300, 308),
            (400, 452),
            (499, 512),
            (599, 600),
        )

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.command(
        name="httpcat",
        description="Get An HTTP Cat Image",
        brief="httpcat 404\nhttpcat 200",
    )
    @commands.guild_only()
    async def httpcat(
        self, ctx: commands.Context, code: Union[int, str]
    ) -> None:

        title = None

        in_valid_range = any(
            code in range(*i) for i in self.HTTP_ERROR_VALID_RANGES
        )

        if code is None:
            code = 400
            title = "Ask with a code"

        elif isinstance(code, str):
            code = 422
            title = "Invalid number code"

        elif not in_valid_range:
            code = 404
            title = "Can't find that code..."

        url = f"https://http.cat/{code}"
        if not title:
            title = str(code)

        embed = discord.Embed(title=title, color=Colors.SUCCESS)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(
        name="urban",
        aliases=["define"],
        description="Get Urban Definition Of An Word",
        brief="urban Mai\nurban Discord",
    )
    async def urban(self, ctx: commands.Context, word: Optional[str]) -> None:

        if not word:
            word = "urban"

        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        headers = {
            "x-rapidapi-key": config["X_RAPID_API_KEY"],
            "x-rapidapi-host": config["X_RAPID_API_HOST"],
        }
        querystring = {"term": f"{word}"}

        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                    url, headers=headers, params=querystring
                ) as r:
                    data = await r.json()

                    try:
                        data = data.get("list")
                        data = data[0]
                    except IndexError:
                        embed = discord.Embed(
                            title="",
                            description="❌ Error: Nothing Found!",
                            colour=Colors.ERROR,
                        )
                        await ctx.send(embed=embed)
                        return

                    definition = data.get("definition")
                    example = data.get("example")
                    thumbs_up = data.get("thumbs_up")
                    thumbs_down = data.get("thumbs_down")

        if not example:
            example = "..."
        elif not definition:
            definition = "There is no definition for this word!"

        embed = discord.Embed(
            title=f"Definition of **{word}**",
            description=definition,
            colour=Colors.SUCCESS,
            timestamp=ctx.message.created_at,
        )

        embed.add_field(name="Examples:", value=example, inline=False)

        embed.add_field(name=":thumbsup:", value=thumbs_up)
        embed.add_field(name=":thumbsdown:", value=thumbs_down)

        embed.set_thumbnail(
            url="https://images-ext-2.discordapp.net/external/HMmIAukJm0YaGc2BKYGx5MuDJw8LUbwqZM9BW9oey5I/https/i.imgur.com/VFXr0ID.jpg"
        )

        embed.set_footer(text=f"Requested by {ctx.author}")
        await ctx.send(embed=embed)

    @urban.error
    async def urban_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(
                title="😢 There was an error!",
                description="Length of the text exceeds discord's limit!",
                colour=Colors.ERROR,
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
