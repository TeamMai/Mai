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
import discord

import pycordSuperUtils

from typing import Optional
from discord.ext import commands
from pycordSuperUtils import MusicManager


from helpers.constants import *
from helpers.logging import log
from helpers.custommeta import CustomCog as Cog

from config.ext.parser import config


class Music(
    Cog,
    pycordSuperUtils.CogManager.Cog,
    name="Music",
    description="Play Spotify, Youtube, SoundCloud",
    emoji=Emoji.MUSIC,
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.skip_votes = {}
        self.MusicManager = MusicManager(self.bot, client_id=config["SPOTIFY_CLIENT_ID"], client_secret=config["SPOTIFY_CLIENT_SECRET"], spotify_support=True)
        self.SEARCH_EMOJI = ":mag_right:"
        self.YOUTUBE_EMBED_COLOR = 0xFF0000
        self.SPOTIFY_EMBED_COLOR = 0x1CAC78
        self.SOUNDCLOUD_EMBED_COLOR = 0xFF7538

    async def get_user_spotify(self, member: discord.Member) -> Optional[discord.Spotify]:
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

    async def parse_count(self, count):
        original_count = count

        count = float("{:.3g}".format(count))
        magnitude = 0
        matches = ["", "K", "M", "B", "T", "Qua", "Qui"]

        while abs(count) >= 1000:
            if magnitude >= 5:
                break

            magnitude += 1
            count /= 1000.0

        try:
            return "{}{}".format(
                "{:f}".format(count).rstrip("0").rstrip("."), matches[magnitude]
            )
        except IndexError:
            return original_count

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @pycordSuperUtils.CogManager.event(pycordSuperUtils.MusicManager)
    async def on_music_error(self, ctx: commands.Context, error):
        if isinstance(error, pycordSuperUtils.NotPlaying):
            pass
        elif isinstance(error, pycordSuperUtils.NotConnected):
            pass



    @pycordSuperUtils.CogManager.event(pycordSuperUtils.MusicManager)
    async def on_play(self, ctx: commands.Context, player):
        # Extracting useful data from player object
        print("hi")
        print(player)
        await ctx.send(player)
        thumbnail = player.data["videoDetails"]["thumbnail"]["thumbnails"][-1]["url"]
        uploader = player.data["videoDetails"]["author"]
        requester = player.requester.mention if player.requester else "Autoplay"

        embed = discord.Embed(
            title="Now Playing",
            color=discord.Color.from_rgb(255, 255, 0),
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            description=f"[**{player.title}**]({player.url}) by **{uploader}**",
        )
        embed.add_field(name="Requested by", value=requester)
        embed.set_thumbnail(url=thumbnail)

        await ctx.send(embed=embed)
        # Clearing skip votes for each song
        if self.skip_votes.get(ctx.guild.id):
            self.skip_votes.pop(ctx.guild.id)

    @pycordSuperUtils.CogManager.event(pycordSuperUtils.MusicManager)
    async def on_queue_end(self, ctx):
        print(f"The queue has ended in {ctx}")
        # You could wait and check activity, etc...

    @pycordSuperUtils.CogManager.event(pycordSuperUtils.MusicManager)
    async def on_inactivity_disconnect(self, ctx):
        print(f"I have left {ctx} due to inactivity..")

    @commands.command()
    @commands.guild_only()
    async def join(self, ctx: commands.Context) -> None:
        if ctx.author.voice is None:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} {ctx.author.mention}, You are not connected to any voice channels.",
            )
            await ctx.send(embed=embed)
            return

        if ctx.guild.me.voice is not None:
            if ctx.guild.me.voice.channel == ctx.author.voice.channel:
                embed = discord.Embed(
                    color=Colors.ERROR,
                    description=f"{Emoji.ERROR} **I am already connected to** `{ctx.author.voice.channel.name}`",
                )
                await ctx.send(embed=embed)
                return

            if ctx.guild.me.voice.channel != ctx.author.voice.channel:
                embed = discord.Embed(
                    color=Colors.ERROR,
                    description=f"{Emoji.ERROR} **I am already connected to another voice channel:** `{ctx.guild.me.voice.channel.name}`",
                )
                await ctx.send(embed=embed)
                return

        if await self.MusicManager.join(ctx):
            await ctx.send(
                f"{Emoji.INFORMATION} **Successfully connected to `{ctx.channel.name}`**"
            )

    @commands.command()
    @commands.guild_only()
    async def leave(self, ctx: commands.Context) -> None:
        if ctx.author.voice is None:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} {ctx.author.mention}, You are not connected to any voice channels.",
            )
            await ctx.send(embed=embed)
            return

        if ctx.voice_client is None:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} **I am not connected to any voice channels!**",
            )
            await ctx.send(embed=embed)
            return

        if ctx.guild.me.voice.channel != ctx.author.voice.channel:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} **Cannot leave because I am in another voice channel** `{ctx.guild.me.voice.channel.name}`",
            )
            await ctx.send(embed=embed)
            return

        loading_embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"{Emoji.LOADING_CIRCLE} Terminating Voice Client",
        )
        message = await ctx.send(embed=loading_embed)

        if await self.MusicManager.leave(ctx):
            completed_embed = discord.Embed(
                color=Colors.SUCCESS,
                description=f"{Emoji.WHITE_CHECKMARK} Successfully Terminated Voice Client",
            )
            await message.edit(content=None, embed=completed_embed)

    @commands.command()
    async def np(self, ctx: commands.Context):
        if player := await self.MusicManager.now_playing(ctx):
            # Played duration
            duration_played = await self.MusicManager.get_player_played_duration(
                ctx, player
            )

            # Loop status
            loop = (await self.MusicManager.get_queue(ctx)).loop
            if loop == pycordSuperUtils.Loops.LOOP:
                loop_status = "Looping enabled."
            elif loop == pycordSuperUtils.Loops.QUEUE_LOOP:
                loop_status = "Queue looping enabled."
            else:
                loop_status = "Looping Disabled"

            # Fecthing other details
            thumbnail = player.data["videoDetails"]["thumbnail"]["thumbnails"][-1][
                "url"
            ]
            title = player.title
            url = player.url
            uploader = player.data["videoDetails"]["author"]
            views = player.data["videoDetails"]["viewCount"]
            requester = player.requester.mention if player.requester else "Autoplay"

            embed = discord.Embed(
                title="Now playing",
                description=f"**{title}**",
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.from_rgb(0, 255, 255),
            )
            embed.add_field(
                name="Played",
                value=self.MusicManager.parse_duration(
                    duration=duration_played, hour_format=False
                ),
            )
            embed.add_field(
                name="Duration",
                value=self.MusicManager.parse_duration(
                    duration=player.duration, hour_format=False
                ),
            )
            embed.add_field(name="Loop", value=loop_status)
            embed.add_field(name="Requested by", value=requester)
            embed.add_field(name="Uploader", value=uploader)
            embed.add_field(name="URL", value=f"[Click]({url})")
            embed.add_field(name="Views", value=await self.parse_count(int(views)))
            embed.set_thumbnail(url=thumbnail)
            embed.set_image(url=r"https://i.imgur.com/ufxvZ0j.gif")
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed)

    @commands.command()
    async def play(self, ctx: commands.Context, *, query: str):
        if not ctx.voice_client or not ctx.voice_client.is_connected():
            await self.MusicManager.join(ctx)

        async with ctx.typing():
            players = await self.MusicManager.create_player(query, ctx.author)

        if players:
            if await self.MusicManager.queue_add(
                players=players, ctx=ctx
            ) and not await self.MusicManager.play(ctx):
                await ctx.send("Song Added To Queue")

        else:
            await ctx.send("Query not found.")

    
    @commands.command()
    async def pause(self, ctx):
        if await self.MusicManager.pause(ctx):
            await ctx.send("Player paused.")

    @commands.command()
    async def resume(self, ctx):
        if await self.MusicManager.resume(ctx):
            await ctx.send("Player resumed.")

    @commands.command()
    async def volume(self, ctx, volume: int):
        await self.MusicManager.volume(ctx, volume)

    @commands.command()
    async def loop(self, ctx):
        is_loop = await self.MusicManager.loop(ctx)
        await ctx.send(f"Looping toggled to {is_loop}")

    @commands.command()
    async def stop(self, ctx):
        await self.MusicManager.cleanup(voice_client=None, guild=ctx.guild)
        ctx.voice_client.stop()
        await ctx.send("⏹️")

    # Spotify song from user
    @commands.command()
    async def play_user_spotify(self, ctx, member: discord.Member = None):
        member = member if member else ctx.author
        spotify_result = await self.get_user_spotify(member)

        if not spotify_result:
            await ctx.send(f"{member.mention} is not listening to Spotify.")
            return

        query = f"{spotify_result.title} {spotify_result.artist}"

        # Calling the play function
        await Music.play_cmd(self, ctx, query)

    @commands.command()
    async def shuffle(self, ctx):
        is_shuffle = await self.MusicManager.shuffle(ctx)

        if is_shuffle is not None:
            await ctx.send(f"Shuffle toggled to {is_shuffle}")

    @commands.command()
    async def previous(self, ctx, index: int = None):

        if previous_player := await self.MusicManager.previous(
            ctx, index, no_autoplay=True
        ):
            await ctx.send(f"Rewinding from {previous_player[0].title}")

    @commands.command()
    async def queueloop(self, ctx):
        is_loop = await self.MusicManager.queueloop(ctx)
        await ctx.send(f"Queue looping toggled to {is_loop}")

    @commands.command()
    async def history(self, ctx):
        formatted_history = [
            f"Title: '{x.title}'\nRequester: {x.requester.mention}"
            for x in (await self.MusicManager.get_queue(ctx)).history
        ]

        embeds = pycordSuperUtils.generate_embeds(
            formatted_history,
            "Song History",
            "Shows all played songs",
            25,
            string_format="{}",
        )

        page_manager = pycordSuperUtils.PageManager(ctx, embeds, public=True)
        await page_manager.run()

    @commands.command()
    async def skip(self, ctx, index: int = None):
        if queue := (await self.MusicManager.get_queue(ctx)):

            requester = (await self.MusicManager.now_playing(ctx)).requester

            # Checking if the song is autoplayed
            if requester is None:
                await ctx.send("Skipped autoplayed song")
                await self.MusicManager.skip(ctx, index)

            # Checking if queue is empty and autoplay is disabled
            elif not queue.queue and not queue.autoplay:
                await ctx.send("Can't skip the last song of queue.")

            else:
                # Checking if guild id list is in skip votes dictionary
                if not self.skip_votes.get(ctx.guild.id):
                    self.skip_votes[ctx.guild.id] = []

                # Checking the voter
                voter = ctx.author

                # If voter is requester than skips automatically
                if voter == (await self.MusicManager.now_playing(ctx)).requester:
                    skipped_player = await self.MusicManager.skip(ctx, index)

                    await ctx.send("Skipped by requester")

                    if not skipped_player.requester:
                        await ctx.send("Autoplaying next song.")

                    # clearing the skip votes
                    self.skip_votes.pop(ctx.guild.id)

                # Voting
                elif (
                    voter.id not in self.skip_votes[ctx.guild.id]
                ):  # Checking if someone already voted
                    # Adding the voter id to skip votes
                    self.skip_votes[ctx.guild.id].append(voter.id)

                    # Calculating total votes
                    total_votes = len(self.skip_votes[ctx.guild.id])

                    # If total votes >=3 then it will skip
                    if total_votes >= 3:
                        skipped_player = await self.MusicManager.skip(ctx, index)

                        await ctx.send("Skipped on vote")

                        if not skipped_player.requester:
                            await ctx.send("Autoplaying next song.")

                        # Clearing skip votes of the guild
                        self.skip_votes.pop(ctx.guild.id)

                    # Shows voting status
                    else:
                        await ctx.send(
                            f"Skip vote added, currently at **{total_votes}/3**"
                        )

                # If someone uses vote command twice
                else:
                    await ctx.send("You have already voted to skip this song.")

    @commands.command()
    async def queue(self, ctx):
        formatted_queue = [
            f"Title: '{x.title}\nRequester: {x.requester.mention}"
            for x in (await self.MusicManager.get_queue(ctx)).queue
        ]

        embeds = pycordSuperUtils.generate_embeds(
            formatted_queue,
            "Queue",
            f"Now Playing: {await self.MusicManager.now_playing(ctx)}",
            25,
            string_format="{}",
        )

        page_manager = pycordSuperUtils.PageManager(ctx, embeds, public=True)
        await page_manager.run()

    @commands.command()
    async def lyrics(self, ctx, *, query=None):
        if response := await self.MusicManager.lyrics(ctx, query):
            # If lyrics are found
            title, author, query_lyrics = response
            # Formatting the lyrics
            splitted = query_lyrics.split("\n")
            res = []
            current = ""
            for i, split in enumerate(splitted):
                if len(splitted) <= i + 1 or len(current) + len(splitted[i + 1]) > 1024:
                    res.append(current)
                    current = ""
                    continue
                current += split + "\n"
            # Creating embeds list for PageManager
            embeds = [
                discord.Embed(
                    title=f"Lyrics for '{title}' by '{author}', (Page {i + 1}/{len(res)})",
                    description=x,
                )
                for i, x in enumerate(res)
            ]
            # editing the embeds
            for embed in embeds:
                embed.timestamp = datetime.datetime.utcnow()

            page_manager = pycordSuperUtils.PageManager(
                ctx,
                embeds,
                public=True,
            )

            await page_manager.run()

        else:
            await ctx.send("No lyrics were found for the song")

    


def setup(bot):
    bot.add_cog(Music(bot))
