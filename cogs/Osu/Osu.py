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
import re
import humanize
import osutools
import datetime

from typing import Optional

from discord.ext import commands
from discord.ext.commands import BucketType


from ossapi.ossapiv2 import OssapiV2
from ossapi.enums import RankStatus, Grade

from osutools.oppai import Oppai

from config.ext.parser import config

from db.models import OSU, Guild

from helpers.constants import *
from helpers.logging import log
from helpers.utils import shorten_url
from helpers.custommeta import CustomCog as Cog

from tortoise.exceptions import TransactionManagementError

osu_v1 = osutools.OsuClientV1(config["OSU_API_V1_KEY"])

if config["USE_DOCKER"]:
    osu_v2 = OssapiV2(
        config["OSU_API_V2_CLIENT_ID"],
        config["OSU_API_V2_CLIENT_SECRET"],
    )
else:
    osu_v2 = OssapiV2(
        config["OSU_API_V2_CLIENT_ID"],
        config["OSU_API_V2_CLIENT_SECRET"],
        config["OSU_API_V2_CLIENT_CALLBACK_URL"],
    )


class StatsFlags(commands.FlagConverter, delimiter=" ", prefix="-"):
    d: Optional[str]  # Detailed


class RecommendFlags(commands.FlagConverter, delimiter=" ", prefix="-"):
    stars: Optional[float]  # 5.0
    time: Optional[float]  # 1m | 50s | 1h
    ar: Optional[float]  # Approach Rate
    od: Optional[float]  # Overall Difficulty
    hp: Optional[float]  # 3
    cs: Optional[float]  # Circle Size
    pp: Optional[float]  # 100
    mods: Optional[str]  # DTHDHRFL


class Osu(
    Cog, name="Osu!", description="Helpful osu! Commands.", emoji=Emoji.OSU
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def fetch_db_username(self, ctx: commands.Context) -> str:
        guild = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]
        osu_model = (
            await OSU.get_or_create(guild=guild, discord_id=ctx.author.id)
        )[0]
        username = osu_model.username
        return username

    async def parse_score(self, score: str) -> str:
        if score == Grade.B:
            return OsuEmotes.B
        elif score == Grade.F:
            return OsuEmotes.F
        elif score == Grade.D:
            return OsuEmotes.D
        elif score == Grade.C:
            return OsuEmotes.C
        elif score == Grade.A:
            return OsuEmotes.A
        elif score == Grade.S:
            return OsuEmotes.S
        elif score == Grade.SH:
            return OsuEmotes.SHD
        elif score == Grade.SSH:
            return OsuEmotes.SSHD
        else:
            return score

    async def parse_playstyle(self, user_playstyle: int) -> str:

        if user_playstyle == 1:
            playstyle = "mouse"
        elif user_playstyle == 2:
            playstyle = "keyboard"
        elif user_playstyle == 3:
            playstyle = "mouse, keyboard"
        elif user_playstyle == 4:
            playstyle = "tablet"
        elif user_playstyle == 5:
            playstyle = "mouse, tablet"
        elif user_playstyle == 6:
            playstyle = "keyboard, tablet"
        elif user_playstyle == 7:
            playstyle = "mouse, keyboard, tablet"
        elif user_playstyle == 8:
            playstyle = "tablet"
        elif user_playstyle == 9:
            playstyle = "mouse, touch"
        elif user_playstyle == 10:
            playstyle = "keyboard, touch"
        elif user_playstyle == 11:
            playstyle = "mouse, keyboard, touch"
        elif user_playstyle == 12:
            playstyle = "tablet, touch"
        elif user_playstyle == 15:
            playstyle = "mouse, keyboard, tablet, touch"
        else:
            playstyle = "None."

        return playstyle

    async def parse_rank_status(self, type: RankStatus) -> str:
        if type == RankStatus.RANKED:
            rank = "Ranked"
        elif type == RankStatus.APPROVED:
            rank = "Approved"
        elif type == RankStatus.GRAVEYARD:
            rank = "Graveyard"
        elif type == RankStatus.LOVED:
            rank = "Loved"
        elif type == RankStatus.QUALIFIED:
            rank = "Qualified"
        elif type == RankStatus.PENDING:
            rank = "Pending"
        elif type == RankStatus.WIP:
            rank = "Work In Progress"
        else:
            rank = "None."

        return rank

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:

        guild = (await Guild.get_or_create(discord_id=message.guild.id))[0]

        try:
            osu = (await OSU.get_or_create(guild=guild))[0]
        except TransactionManagementError:
            pass

        beatmap_regex = re.compile(r"https://osu\.ppy\.sh/b/?(\d+)$")
        beatmap_regex_match = beatmap_regex.search(message.content)
        if beatmap_regex_match and osu.passive:

            regex_beatmap_id = beatmap_regex_match.group(1)

            beatmap_id = int(regex_beatmap_id)

            await message.channel.send(beatmap_id)

        user_regex = re.compile(r"https://osu\.ppy\.sh/users/?(\d+)$")
        user_regex_match = user_regex.search(message.content)
        if user_regex_match and osu.passive:

            user_id = user_regex_match.group(1)

            user = osu_v1.fetch_user(user_id=user_id)

            delta = datetime.timedelta(seconds=user.playtime)
            playtime = humanize.precisedelta(
                delta, suppress=["days"], minimum_unit="hours", format="%0.0f"
            )

            embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"{Chars.ARROW} **Bancho Rank:** #{humanize.intcomma(user.rank)} ({user.country}#{humanize.intcomma(user.country_rank)})\n{Chars.ARROW} **Level:** {int(round(user.level ,2))}%\n{Chars.ARROW} **PP:** {humanize.intcomma(user.pp)} **Acc:** {round(user.accuracy, 2)}%\n{Chars.ARROW} **Playcount:** {humanize.intcomma(user.play_count)} ({playtime})\n{Chars.ARROW} **Ranks:** {OsuEmotes.SSHD}`{user.ssh_count}`{OsuEmotes.SS}`{user.ss_count}`{OsuEmotes.S}`{user.s_count}`{OsuEmotes.A}`{user.a_count}`",
            )
            embed.set_author(
                name=f"Osu Standard Profile for {user.username}",
                url=f"https://osu.ppy.sh/users/{user.id}",
                icon_url=f"https://osu.ppy.sh/images/flags/{user.country}.png",
            )
            embed.set_thumbnail(url=user.avatar_url)

            embed.set_footer(
                text=f"On osu! Bancho | User ID: {user.id}",
                icon_url=OsuEmotes.OSU_LOGO_IMAGE,
            )

            await message.channel.send(embed=embed)

    @commands.group(
        invoke_without_subcommand=True, description="Manage Osu Commands"
    )
    @commands.guild_only()
    async def osu(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)
            return

    @commands.cooldown(1, 5, BucketType.user)
    @osu.command(
        name="link",
        aliases=["set"],
        description="Link your osu account to your discord account.",
        extras={"Examples": "osu link Whitecat\nosu set Whitecat"},
    )
    async def osu_link(self, ctx: commands.Context, *, username: str) -> None:

        guild = (await Guild.get_or_create(ctx.guild.id))[0]

        if await OSU.exists(guild=guild, discord_id=ctx.author.id):

            await OSU.filter(guild=guild, discord_id=ctx.author.id).update(
                username=username
            )

            embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"{Emoji.CHECKMARK} **Successfully Updated Username To:** `{username}`",
            )
            await ctx.send(embed=embed)
        else:
            await OSU.create(
                guild=guild, discord_id=ctx.author.id, username=username
            )
            embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"{Emoji.CHECKMARK} **Successfully Created Username:** `{username}`",
            )
            await ctx.send(embed=embed)

    @commands.cooldown(1, 5, BucketType.user)
    @osu.command(
        name="stats",
        description="Get Basic Stats About A Player",
        extras={"Examples": "osu stats Whitecat`\n`osu stats Whitecat -d yes"},
    )
    async def osu_stats(
        self,
        ctx: commands.Context,
        username: Optional[str],
        *,
        StatsFlags: StatsFlags,
    ) -> None:

        if username is None:
            username = await self.fetch_db_username(ctx)

        user_v1 = osu_v1.fetch_user(username=username)

        if user_v1 is None:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} **The user {username} was not found!**",
            )
            await ctx.send(embed=embed)
            return

        # NOTE: I run my own local version of osutools, so If you get an error from these two lines, change

        # ----------------------------------------------------

        # osutools/user.py
        # seconds = int(user_info["total_seconds_played"])
        # self.playtime = Playtime(seconds)

        # TO ⬇

        # seconds = int(user_info['total_seconds_played'])
        # self.playtime = seconds

        # ----------------------------------------------------

        delta = datetime.timedelta(seconds=user_v1.playtime)
        playtime = humanize.precisedelta(
            delta, suppress=["days"], minimum_unit="hours", format="%0.0f"
        )

        # DISCLAIMER: This Embed Style Has Been Recreated/Copied From https://github.com/AznStevy/owo-bot/, All Credits Goes To Him.

        if StatsFlags.d:

            user_v2 = osu_v2.user(username)

            embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"{Chars.ARROW} **Bancho Rank:** #{humanize.intcomma(user_v1.rank)} ({user_v1.country}#{humanize.intcomma(user_v1.country_rank)})\n{Chars.ARROW} **Level:** {int(round(user_v1.level ,2))}%\n{Chars.ARROW} **PP:** {humanize.intcomma(user_v1.pp)} **Acc:** {round(user_v1.accuracy, 2)}%\n{Chars.ARROW} **Playcount:** {humanize.intcomma(user_v1.play_count)} ({playtime})\n{Chars.ARROW} **Ranks:** {OsuEmotes.SSHD}`{user_v1.ssh_count}`{OsuEmotes.SS}`{user_v1.ss_count}`{OsuEmotes.S}`{user_v1.s_count}`{OsuEmotes.A}`{user_v1.a_count}`\n{Chars.ARROW} **Ranked Score:** {humanize.intcomma(user_v1.ranked_score)}\n{Chars.ARROW} **Total Score:** {humanize.intcomma(user_v1.total_score)}\n{Chars.ARROW} **Total Hits:** {humanize.intcomma(user_v1.num_300 + user_v1.num_100 + user_v1.num_50)}\n{Chars.ARROW} **Max Combo:** {humanize.intcomma(user_v2.statistics.maximum_combo)}",
            )

            if user_v2.twitter is None:
                twitter = "No Twitter."
            else:
                twitter = f"[{user_v2.twitter}]({user_v2.twitter})"

            if user_v2.discord is None:
                osu_discord = "No Discord."
            else:
                osu_discord = user_v2.discord

            embed.add_field(
                name="Contact",
                value=f"{Chars.ARROW} **Discord:** {osu_discord} \n{Chars.ARROW} **Twitter:** {twitter}",
                inline=False,
            )

            embed.add_field(
                name="Extra Info",
                value=f"{Chars.ARROW} **Previously Known As:** {' , '.join(user_v2.previous_usernames)}  \n{Chars.ARROW} **Playstyle:**: {await self.parse_playstyle(user_v2.playstyle)} \n{Chars.ARROW} **Followers:** {humanize.intcomma(user_v2.follower_count)} \n{Chars.ARROW} **Ranked/Approved Beatmaps:** {humanize.intcomma(user_v2.ranked_and_approved_beatmapset_count)} \n{Chars.ARROW} **Replays Watched By Others:** {humanize.intcomma(user_v2.statistics.replays_watched_by_others)}",
                inline=False,
            )

            embed.set_author(
                name=f"Osu Standard Profile for {user_v1.username}",
                url=f"https://osu.ppy.sh/users/{user_v1.id}",
                icon_url=f"https://osu.ppy.sh/images/flags/{user_v1.country}.png",
            )
            embed.set_thumbnail(url=user_v1.avatar_url)
            embed.set_image(url=user_v2.cover_url)

            embed.set_footer(
                text=f"On osu! Bancho | User ID: {user_v1.id}",
                icon_url=OsuEmotes.OSU_LOGO_IMAGE,
            )

            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"{Chars.ARROW} **Bancho Rank:** #{humanize.intcomma(user_v1.rank)} ({user_v1.country}#{humanize.intcomma(user_v1.country_rank)})\n{Chars.ARROW} **Level:** {int(round(user_v1.level ,2))}%\n{Chars.ARROW} **PP:** {humanize.intcomma(user_v1.pp)} **Acc:** {round(user_v1.accuracy, 2)}%\n{Chars.ARROW} **Playcount:** {humanize.intcomma(user_v1.play_count)} ({playtime})\n{Chars.ARROW} **Ranks:** {OsuEmotes.SSHD}`{user_v1.ssh_count}`{OsuEmotes.SS}`{user_v1.ss_count}`{OsuEmotes.S}`{user_v1.s_count}`{OsuEmotes.A}`{user_v1.a_count}`",
            )
            embed.set_author(
                name=f"Osu Standard Profile for {user_v1.username}",
                url=f"https://osu.ppy.sh/users/{user_v1.id}",
                icon_url=f"https://osu.ppy.sh/images/flags/{user_v1.country}.png",
            )
            embed.set_thumbnail(url=user_v1.avatar_url)

            embed.set_footer(
                text=f"On osu! Bancho | User ID: {user_v1.id}",
                icon_url=OsuEmotes.OSU_LOGO_IMAGE,
            )

        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, BucketType.user)
    @osu.command(
        name="recent",
        aliases=["rs"],
        description="Get A user's most recent play",
        extras={"Examples": "osu recent Whitecat\n-osu recent\n-osu rs"},
    )
    async def recent(
        self, ctx: commands.Context, *, username: Optional[str]
    ) -> None:

        if username is None:
            username = await self.fetch_db_username(ctx)

        user = osu_v2.user(user=username)

        user_recents_v2 = osu_v2.user_scores(user.id, type_="recent")

        user_recent = user_recents_v2[0]

        pp = round(user_recent.pp, 2) if user_recent.pp is not None else "0"

        embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"{Chars.ARROW} {await self.parse_score(user_recent.rank)} **{Chars.ARROW} {pp} PP** {Chars.ARROW} {round(user_recent.accuracy, 2)}%\n{Chars.ARROW} {humanize.intcomma(user_recent.score)} {Chars.ARROW} TEST/{user_recent.max_combo}",
        )

        embed.set_author(
            name=f"{user_recent.beatmapset.title} [{user_recent.beatmap.version}] + {user_recent.mods} [{user_recent.beatmap.difficulty_rating}{OsuEmotes.STAR_ICON}]",
            url=f"https://osu.ppy.sh/b/{user_recent.beatmapset.id}",
            icon_url=user.avatar_url,
        )
        embed.set_thumbnail(
            url=f"https://b.ppy.sh/thumb/{user_recent.beatmapset.id}l.jpg"
        )
        embed.set_footer(
            text=f"On osu! Bancho | User ID: {user.id}",
            icon_url=OsuEmotes.OSU_LOGO_IMAGE,
        )
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, BucketType.user)
    @osu.command(
        name="recommend",
        aliases=["r"],
        description="Recommend A Map Based On A Few Variables",
    )
    async def recommend(
        self,
        ctx: commands.Context,
        username: Optional[str],
        *,
        RecommendFlags: RecommendFlags,
    ) -> None:
        pass

    @commands.cooldown(1, 5, BucketType.user)
    @osu.command(
        name="scores", description="Get scores of a player on a beatmap"
    )
    async def scores(
        self,
        ctx: commands.Context,
        username: Optional[str],
        beatmap: Optional[str],
    ) -> None:
        pass

    @commands.cooldown(1, 5, BucketType.user)
    @osu.command(name="compare", aliases=["c"], description="Compare 2 Players")
    async def compare(
        self,
        ctx: commands.Context,
        username: Optional[str],
        username2: Optional[str],
    ) -> None:
        pass

    @commands.cooldown(1, 5, BucketType.user)
    @osu.command(
        name="top", aliases=["t"], description="Get The Top 5 Plays Of Any User"
    )
    async def top(
        self, ctx: commands.Context, *, username: Optional[str]
    ) -> None:
        pass

    @commands.cooldown(1, 5, BucketType.user)
    @osu.command(
        name="map", aliases=["m"], description="Display Stats About A Map"
    )
    async def map(
        self, ctx: commands.Context, *, beatmap: Optional[str]
    ) -> None:
        pass

    @commands.cooldown(1, 5, BucketType.user)
    @osu.command(name="whatif", description="Get The Top 5 Plays Of Any User")
    async def whatif(
        self, ctx: commands.Context, username: Optional[str], pp: Optional[int]
    ) -> None:
        pass

    @commands.cooldown(1, 5, BucketType.user)
    @osu.command(
        name="fix",
        description="Display A User's PP After Unchoking Their Score On A Map",
    )
    async def fix(
        self,
        ctx: commands.Context,
        username: Optional[str],
        beatmap: Optional[str],
    ) -> None:
        pass

    @commands.cooldown(1, 5, BucketType.user)
    @osu.command(
        name="avatar",
        aliases=["av"],
        description="Get The Avatar Of A User",
        extras={"Examples": "osu avatar\n-osu avatar Whitecat\n-osu av Whitecat"},
    )
    async def osu_avatar(
        self, ctx: commands.Context, *, username: Optional[str]
    ) -> None:

        if username is None:
            username = await self.fetch_db_username(ctx)

        user = osu_v1.fetch_user(username=username)

        embed = discord.Embed(color=Colors.DEFAULT)
        embed.set_author(
            name=f"{user}",
            url=f"https://osu.ppy.sh/users/{user.id}",
            icon_url=f"https://osu.ppy.sh/images/flags/{user.country}.png",
        )
        embed.set_image(url=user.avatar_url)

        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, BucketType.user)
    @osu.command(
        name="skin",
        description="Set Your Favorite Skin",
        extras={"Examples": "osu skin https://skins.osuck.net/index.php?newsid=1648"},
    )
    async def skin(self, ctx: commands.Context, skin: Optional[str]) -> None:

        guild = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]

        if skin is None:
            osu = (
                await OSU.get_or_create(guild=guild, discord_id=ctx.author.id)
            )[0]
            skin = osu.skin

            embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"**Your Current Skin:** {skin}",
            )
            await ctx.send(embed=embed)
            return

        if not skin.startswith("https://skins.osuck.net/"):
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} `skin` **REQUIRES A `https://skins.osuck.net/` URL.**",
            )
            await ctx.send(embed=embed)
            return

        if await OSU.exists(guild=guild, discord_id=ctx.author.id):

            url = await shorten_url(str(skin))

            await OSU.filter(guild=guild, discord_id=ctx.author.id).update(
                skin=url
            )

            embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"{Emoji.CHECKMARK} **Successfully Updated Skin**.",
            )
            embed.set_author(
                name=ctx.author.name, icon_url=ctx.author.avatar.url
            )
            embed.add_field(name="Shareable URL", value=f"[URL]({url})")

            await ctx.send(embed=embed)

    @commands.cooldown(1, 10, BucketType.user)
    @commands.has_permissions(administrator=True)
    @osu.command(
        name="passive",
        description="Toggle Passive Mode",
        extras={"Examples": "osu passive True"},
    )
    async def passive(
        self, ctx: commands.Context, passive: Optional[bool]
    ) -> None:

        guild = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]

        if passive is None:
            osu = (
                await OSU.get_or_create(guild=guild, discord_id=ctx.author.id)
            )[0]
            passive = osu.passive

            embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"**Passive Enabled:** `{passive}`",
            )
            await ctx.send(embed=embed)
            return

        if await OSU.exists(guild=guild):

            await OSU.filter(guild=guild).update(passive=passive)

            embed = discord.Embed(
                color=Colors.DEFAULT,
                description=f"{Emoji.CHECKMARK} **Passive set to {passive}**.",
            )
            embed.set_author(
                name=ctx.author.name, icon_url=ctx.author.avatar.url
            )

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Osu(bot))
