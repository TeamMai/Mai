"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import re

import discord
import asyncio
import spotbee

import PycordUtils

from typing import Optional
from discord.ext import commands

from helpers.constants import *
from helpers.logging import log
from helpers.custommeta import CustomCog as Cog

from config.ext.parser import config


class Music(
    Cog,
    name="Music",
    description="Play Spotify, Youtube, SoundCloud",
    emoji=Emoji.MUSIC,
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.music = PycordUtils.Music()
        self.SEARCH_EMOJI = ":mag_right:"
        self.YOUTUBE_EMBED_COLOR = 0xFF0000
        self.SPOTIFY_EMBED_COLOR = 0x1CAC78
        self.SOUNDCLOUD_EMBED_COLOR = 0xFF7538
        self.SPOTIFY_TRACK_RE = re.compile(
            r"^https://open.spotify.com/track/([a-zA-Z0-9]+)"
        )
        self.SPOTIFY_PLAYLIST_RE = re.compile(
            r"^https://open.spotify.com/playlist/([a-zA-Z0-9]+)"
        )

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    async def make_queue_description(self, song):
        text = f"[{song.name}]({song.url}) | `{song.duration}`\n"
        return text

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

        await ctx.author.voice.channel.connect()
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

        completed_embed = discord.Embed(
            color=Colors.SUCCESS,
            description=f"{Emoji.WHITE_CHECKMARK} Successfully Terminated Voice Client",
        )

        await ctx.voice_client.disconnect()
        await message.edit(content=None, embed=completed_embed)

    @commands.command()
    @commands.guild_only()
    async def play(self, ctx: commands.Context, *, url: str) -> None:
        if ctx.author.voice is None:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} {ctx.author.mention}, You are not connected to any voice channels.",
            )
            await ctx.send(embed=embed)
            return

        if ctx.voice_client is None:
            message = await ctx.send(
                f"{Emoji.LOADING_DOTS} **Connecting to** `{ctx.channel.name}`"
            )
            await asyncio.sleep(0.5)
            await ctx.author.voice.channel.connect()
            await message.edit(
                content=f"{Emoji.WHITE_CHECKMARK} **Successfully connected to `{ctx.channel.name}`**"
            )

        message = await ctx.send(
            f"{Emoji.LOADING_DOTS} **Fetching `Music Player`**"
        )
        player = self.music.get_player(
            guild_id=ctx.guild.id, channel_id=ctx.guild.me.voice.channel.id
        )
        if not player:
            await asyncio.sleep(1)
            await message.edit(
                f"{Emoji.ERROR} **`Music Player` does not exist..creating**"
            )
            player = self.music.create_player(ctx, ffmpeg_error_betterfix=True)
            await message.edit(
                f"{Emoji.WHITE_CHECKMARK} **`Music Player` Fetched!**"
            )
        else:
            await asyncio.sleep(0.5)
            await message.edit(
                content=f"{Emoji.WHITE_CHECKMARK} **Fetched `Music Player` successfully!**"
            )
        if not ctx.voice_client.is_playing():
            spotify_playlist_regex_match = self.SPOTIFY_PLAYLIST_RE.search(url)
            if spotify_playlist_regex_match:
                spotify_playlist = spotify_playlist_regex_match.group(0)
                await ctx.send(
                    f"{Emoji.SPOTIFY} **Searching** `{spotify_playlist}`"
                )
                urls = await spotbee.get_songs(
                    config["SPOTIFY_CLIENT_ID"],
                    config["SPOTIFY_CLIENT_SECRET"],
                    spotify_playlist,
                )
                await ctx.send(
                    f"{Emoji.INFORMATION} **`DISCLAIMER`: Playlists may take longer to start playing**"
                )
                message = await ctx.send(
                    f"{Emoji.LOADING_CIRCLE} Adding Songs to Queue..."
                )
                for url in urls:
                    song = await player.queue(url, search=True)
                await message.edit(
                    content=f"{Emoji.SPOTIFY} **Queued All `{len(urls)}` songs!**"
                )
                return

            spotify_track_match = self.SPOTIFY_TRACK_RE.search(url)
            if spotify_track_match:
                spotify_track = spotify_track_match.group(0)
                await ctx.send(
                    f"{Emoji.SPOTIFY} **Searching** `{spotify_track}`"
                )
                url = await spotbee.get_url(spotify_track)
                await ctx.send(url)
                await player.queue(url, search=True)
                song = await player.play()
                await ctx.send(f"{Emoji.SPOTIFY} **Now Playing `{song.name}`**")
                return

            else:
                await ctx.send(
                    f"{Emoji.YOUTUBE} **Searching** {self.SEARCH_EMOJI} `{url}`"
                )
                await player.queue(url, search=True)
                song = await player.play()
                await ctx.send(f"{Emoji.YOUTUBE} **Now Playing** `{song.name}`")
                return
        else:
            spotify_regex_match = self.SPOTIFY_PLAYLIST_RE.search(url)
            if spotify_regex_match:
                spotify_playlist = spotify_regex_match.group(0)
                await ctx.send(
                    f"{Emoji.SPOTIFY} **Searching** `{spotify_playlist}`"
                )
                urls = await spotbee.get_songs(
                    config["SPOTIFY_CLIENT_ID"],
                    config["SPOTIFY_CLIENT_SECRET"],
                    spotify_playlist,
                )
                await ctx.send(
                    f"{Emoji.INFORMATION} **`DISCLAIMER`: Playlists may take longer to start playing**"
                )
                message = await ctx.send(
                    f"{Emoji.LOADING_CIRCLE} Adding Songs to Queue..."
                )
                for url in urls:
                    song = await player.queue(url, search=True)
                await message.edit(
                    content=f"{Emoji.SPOTIFY} **Queued All `{len(urls)}` songs!**"
                )
                return

            spotify_track_match = self.SPOTIFY_TRACK_RE.search(url)
            if spotify_track_match:
                spotify_track = spotify_track_match.group(0)
                await ctx.send(
                    f"{Emoji.SPOTIFY} **Searching** `{spotify_track}`"
                )
                url = await spotbee.get_url(spotify_track)
                song = await player.queue(url, search=True)
                await ctx.send(
                    f"{Emoji.SPOTIFY} **Added `{song.name}` to the queue**"
                )
                return

            else:
                await ctx.send(
                    f"{Emoji.YOUTUBE} **Searching** {self.SEARCH_EMOJI} `{url}`"
                )
                song = await player.queue(url, search=True)
                await ctx.send(
                    f"{Emoji.YOUTUBE} **Added `{song.name}` to the queue**"
                )
                return

    @commands.command()
    async def pause(self, ctx: commands.Context) -> None:
        if ctx.author.voice is None:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} {ctx.author.mention}, You are not connected to any voice channels.",
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

        player = self.music.get_player(
            guild_id=ctx.guild.id, channel_id=ctx.guild.me.voice.channel.id
        )
        song = await player.pause()
        embed = discord.Embed(
            color=Colors.SUCCESS,
            description=f"{Emoji.WHITE_CHECKMARK} **{song.name} Paused**",
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def resume(self, ctx: commands.Context) -> None:
        if ctx.author.voice is None:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} {ctx.author.mention}, You are not connected to any voice channels.",
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

        player = self.music.get_player(
            guild_id=ctx.guild.id, channel_id=ctx.guild.me.voice.channel.id
        )
        song = await player.resume()
        embed = discord.Embed(
            color=Colors.SUCCESS,
            description=f"{Emoji.WHITE_CHECKMARK} **`{song.name}` Resumed**",
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def stop(self, ctx: commands.Context) -> None:
        if ctx.author.voice is None:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} {ctx.author.mention}, You are not connected to any voice channels.",
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

        player = self.music.get_player(
            guild_id=ctx.guild.id, channel_id=ctx.guild.me.voice.channel.id
        )
        await player.stop()
        embed = discord.Embed(
            color=Colors.ERROR,
            description=f"{Emoji.VOICE_CHANNEL} **Stopped Playing Music :(**",
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def loop(self, ctx: commands.Context) -> None:
        if ctx.author.voice is None:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} {ctx.author.mention}, You are not connected to any voice channels.",
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

        player = self.music.get_player(
            guild_id=ctx.guild.id, channel_id=ctx.guild.me.voice.channel.id
        )
        song = await player.toggle_song_loop()
        embed = discord.Embed()
        if song.is_looping:
            embed.description = (
                f"{Emoji.VOICE_CHANNEL} **Enabled Loop For `{song.name}`**"
            )
            embed.color = Colors.SUCCESS
            await ctx.send(embed=embed)
        else:
            embed.description = (
                f"{Emoji.VOICE_CHANNEL} **Disabled Loop For `{song.name}`**"
            )
            embed.color = Colors.ERROR
            await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx: commands.Context) -> None:
        if ctx.author.voice is None:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} {ctx.author.mention}, You are not connected to any voice channels.",
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

        player = self.music.get_player(
            guild_id=ctx.guild.id, channel_id=ctx.guild.me.voice.channel.id
        )

        queue_embed = discord.Embed(
            color=Colors.DEFAULT, title=f"Queue for {ctx.guild.name}"
        )

        queue_embed.description = f"__Queue__:\n{await self.make_queue_description(song for song in player.current_queue())}"

        await ctx.send(embed=embed)

    @commands.command()
    async def np(self, ctx: commands.Context) -> None:
        if ctx.author.voice is None:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} {ctx.author.mention}, You are not connected to any voice channels.",
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

        player = self.music.get_player(
            guild_id=ctx.guild.id, channel_id=ctx.guild.me.voice.channel.id
        )
        song = player.now_playing()
        if song:
            embed = discord.Embed()
            embed.description = f"```\n{song.name}\n```"

            embed.add_field(name="Duration", value=song.length, inline=True)

            embed.set_thumbnail(url=song.thumbnail)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} {ctx.author.mention}**, Nothing is playing!**",
            )
            await ctx.send(embed=embed)
            return

    @commands.command()
    async def skip(self, ctx: commands.Context) -> None:
        if ctx.author.voice is None:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} {ctx.author.mention}, You are not connected to any voice channels.",
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

        player = self.music.get_player(
            guild_id=ctx.guild.id, channel_id=ctx.guild.me.voice.channel.id
        )
        data = await player.skip(force=True)
        if len(data) == 2:
            await ctx.send(f"Skipped {data[0].name}")
        else:
            await ctx.send(f"Skipped {data[0].name}")

    @commands.command()
    async def volume(self, ctx: commands.Context, vol: float) -> None:
        if ctx.author.voice is None:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} {ctx.author.mention}, You are not connected to any voice channels.",
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

        player = self.music.get_player(
            guild_id=ctx.guild.id, channel_id=ctx.guild.me.voice.channel.id
        )
        song, volume = await player.change_volume(
            float(vol) / 100
        )  # volume should be a float between 0 to 1
        await ctx.send(f"Changed volume for {song.name} to {volume*100}%")

    @commands.command()
    async def remove(self, ctx: commands.Context, index: int) -> None:
        if ctx.author.voice is None:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} {ctx.author.mention}, You are not connected to any voice channels.",
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

        player = self.music.get_player(
            guild_id=ctx.guild.id, channel_id=ctx.guild.me.voice.channel.id
        )
        song = await player.remove_from_queue(int(index))
        await ctx.send(f"Removed {song.name} from queue")


def setup(bot):
    bot.add_cog(Music(bot))
