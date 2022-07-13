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
import traceback

from typing import Union
from discord.ext import commands
from discord.ext.commands import BucketType

from helpers.constants import *
from helpers.logging import log
from helpers.cache.reddit import RedditPostCacher
from helpers.custommeta import CustomCog as Cog

from db.models import Guild


class NSFW(
    Cog,
    name="NSFW",
    description="NSFW(Not Safe For Work) Commands :smirk:",
    emoji=Emoji.NSFW,
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.subreddits = (
            "ass",
            "LegalTeens",
            "boobs",
            "pussy",
            "TooCuteForPorn",
            "Nudes",
            "cumsluts",
            "hentai",
        )
        self.cache = RedditPostCacher(
            self.subreddits, "./cogs/NSFW/cache/NSFW.pickle"
        )
        self.cache.cache_posts.start()

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    async def _reddit_sender(
        self, ctx: commands.Context, subrd: str, title: str
    ):
        """Fetches from reddit and sends results
        Parameters
        ----------
        ctx : discord.ext.commands.Context
                The invocation context
        subrd : str
                The subreddit to fetch from
        title : str
                The title to use in the embed
        """
        guild_model = (await Guild.get_or_create(discord_id=ctx.guild.id))[0]

        if guild_model.is_nsfw_disabled:
            embed = discord.Embed(
                description=f"{Emoji.ERROR} `NSFW` Has Been Disabled By Sever Admins."
            )
            await ctx.send(embed=embed)
            return

        submission = await self.cache.get_random_post(subrd)

        embed = discord.Embed(
            title=title,
            timestamp=ctx.message.created_at,
            colour=discord.Color.dark_purple(),
        )
        embed.set_image(url=submission)
        embed.set_footer(text=f"Requested by {ctx.author}")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.NSFWChannelRequired):
            embed = discord.Embed(
                title="NSFW not allowed here",
                description="Use NSFW commands in a NSFW marked channel.",
                color=Colors.ERROR,
            )
            embed.set_image(url=Links.NSFW_CHANNEL_REQUIRED)
            await ctx.send(embed=embed)
        else:
            traceback.print_exception(type(error), error, error.__traceback__)

    @commands.command(name="ass", description="Ass Pictures", extras={"Examples": "ass"})
    @commands.guild_only()
    @commands.is_nsfw()
    async def ass(self, ctx: commands.Context) -> None:
        await self._reddit_sender(ctx, "ass", "DRUMS")

    @commands.command(name="teen", description="Legal Teenagers", extras={"Examples": "teen"})
    @commands.guild_only()
    @commands.is_nsfw()
    async def teen(self, ctx: commands.Context) -> None:
        await self._reddit_sender(ctx, "LegalTeens", "You like them young?")

    @commands.command(name="boobs", description="Boob Pictures", extras={"Examples": "boobs"})
    @commands.guild_only()
    @commands.is_nsfw()
    async def boobs(self, ctx: commands.Context) -> None:
        await self._reddit_sender(ctx, "boobs", "Bounce! Bounce!")

    @commands.command(name="pussy", description="Pussy Pictures", extras={"Examples": "pussy"})
    @commands.guild_only()
    @commands.is_nsfw()
    async def pussy(self, ctx: commands.Context) -> None:
        await self._reddit_sender(ctx, "pussy", "Wet or Dry?")

    @commands.command(
        name="cutesluts", description="Cute Pictures", extras={"Examples": "cutesluts"}
    )
    @commands.guild_only()
    @commands.is_nsfw()
    async def cutesluts(self, ctx: commands.Context) -> None:
        await self._reddit_sender(
            ctx, "TooCuteForPorn", "Too cute for porn, aren't they?"
        )

    @commands.command(name="nudes", description="nude pictures", extras={"Examples": "nudes"})
    @commands.guild_only()
    @commands.is_nsfw()
    async def nudes(self, ctx: commands.Context) -> None:
        await self._reddit_sender(ctx, "Nudes", "Sick of pornstars? Me too!")

    @commands.command(
        name="cum",
        aliases=["cumsluts"],
        description="Cumslut Pictures",
        extras={"Examples": "cum"},
    )
    @commands.guild_only()
    @commands.is_nsfw()
    async def cum(self, ctx: commands.Context) -> None:
        await self._reddit_sender(
            ctx, "cumsluts", "And they don't stop cumming!"
        )

    @commands.command(
        name="hentai", description="Hentai Pictures", extras={"Examples": "hentai"}
    )
    @commands.guild_only()
    @commands.is_nsfw()
    async def hentai(self, ctx: commands.Context) -> None:
        await self._reddit_sender(ctx, "hentai", "AnImE iS jUsT CaRtOoN")

    @commands.group(
        name="nsfw", invoke_without_subcommand=True, description="Manage NSFW"
    )
    async def nsfw(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)
            return

    @commands.guild_only()
    @commands.bot_has_permissions(manage_guild=True)
    @nsfw.command(
        name="toggle",
        description="Toggle NSFW On/Off",
        extras={"Examples": "nsfw toggle on\nnsfw toggle off\nnsfw toggle True\nnsfw toggle False"},
    )
    async def nsfw_toggle(
        self, ctx: commands.Context, toggle: Union[bool, str]
    ) -> None:
        guild = await Guild.get_or_none(discord_id=ctx.guild.id)

        if type(toggle) is str:
            if toggle == "on":
                toggle = True
            elif toggle == "off":
                toggle = False
            elif toggle != "on" or "off":
                embed = discord.Embed(
                    color=Colors.ERROR,
                    description=f"{Emoji.ERROR} `toggle` expects `on`/`off`, not `{str(toggle)}`",
                )
                await ctx.send(embed=embed)
                return

        guild.is_nsfw_disabled = toggle
        await guild.save(update_fields=["is_nsfw_disabled"])
        await guild.refresh_from_db(fields=["is_nsfw_disabled"])

        embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"`NSFW` **Toggled To:** `{toggle}`",
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(NSFW(bot))
