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

from typing import Optional
from discord.ext import commands

from helpers.constants import *
from helpers.logging import log

from helpers.custommeta import CustomCog as Cog


class Spotify(
    Cog,
    name="Spotify",
    description="Get Spotify Information",
    emoji=Emoji.SPOTIFY,
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.command(
        name="spotify",
        description="Get An Image Of What You're Currently Listening Too On Spotify",
        extras={"Examples": "spotify @Member\nspotify (Can Be Used Standalone)"},
    )
    async def spotify(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ) -> None:
        if member is None:
            member = ctx.author

        async with ctx.channel.typing():
            spotify = discord.utils.find(
                lambda a: isinstance(a, discord.Spotify), member.activities
            )

            if spotify is None:
                embed = discord.Embed(
                    color=Colors.ERROR,
                    description=f"{Emoji.ERROR} **{member}** is not listening or connected to Spotify.",
                )
                return await ctx.send(embed=embed)

            image = await self.bot.jeyyapi_client.spotify_from_object(spotify)

            await ctx.send(
                f"> **{member}** is listening to **{spotify.title}**",
                file=discord.File(image, f"{member.name}-spotify.png"),
            )


def setup(bot):
    bot.add_cog(Spotify(bot))
