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
from typing import Optional

import discord
import pycordSuperUtils
from discord.ext import commands
from discord.ext.commands import Bot, BucketType
from pycordSuperUtils import MusicManager

from config.ext.parser import config
from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log


class Music(
    Cog,
    pycordSuperUtils.CogManager.Cog,
    name="Music",
    description="Play Spotify, Youtube, SoundCloud",
    emoji=Emoji.MUSIC,
):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.skip_votes = {}
        self.MusicManager = MusicManager(
            self.bot,
            client_id=config["SPOTIFY_CLIENT_ID"],
            client_secret=config["SPOTIFY_CLIENT_SECRET"],
            spotify_support=True,
        )
        self.SEARCH_EMOJI = ":mag_right:"
        self.YOUTUBE_EMBED_COLOR = 0xFF0000
        self.SPOTIFY_EMBED_COLOR = 0x1CAC78
        self.SOUNDCLOUD_EMBED_COLOR = 0xFF7538

    async def get_user_spotify(
        self, member: discord.Member
    ) -> Optional[discord.Spotify]:
        """
        Returns the member's spotify activity, if applicable
        :param discord.Member member: The member.
        :return: The member's spotify activity.
        :rtype: Optional[discord.Spotify]
        """

        return next(
            (
                activity
                for activity in member.activities
                if isinstance(activity, discord.Spotify)
            ),
            None,
        )

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

def setup(bot) -> None:
    bot.add_cog(Music(bot))
