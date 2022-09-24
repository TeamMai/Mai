"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

from typing import Optional

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Bot, BucketType

from db.models import Counting, Guild
from helpers.constants import *
from helpers.custommeta import CustomCog as Cog
from helpers.logging import log
from helpers.types import *


class CountingCog(
    Cog,
    name="Counting",
    description="Count To A Number, The Right Way!",
    emoji=Emoji.COUNTING,
):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(
        manage_channels=True, manage_messages=True, manage_webhooks=True
    )
    @commands.group(invoke_without_command=True, description="Manage Counting Settings")
    @commands.guild_only()
    async def counting(self, ctx: commands.Context) -> None:

        counting = await Counting.get_or_none(guild__discord_id=ctx.guild.id)

        if counting:
            if counting.enabled:
                channel = ctx.guild.get_channel(counting.counting_channel)
                embed = discord.Embed(
                    color=Colors.SUCCESS,
                    description=f"Counting has been enabled in this server and the counting channel is {channel.mention}!",
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    color=Colors.DEFAULT,
                    description=f"Counting has been disabled in this server!",
                )
                await ctx.send(embed=embed)
            return
        await ctx.send_help(ctx.command)

    @counting.command(
        name="stats",
        aliases=["info"],
        description="Get All Current Counting Stats",
    )
    async def counting_stats(self, ctx: commands.Context) -> None:

        guild = await Guild.from_context(ctx)
        counting = await Counting.get_or_none(guild=guild)

        if not counting:
            embed = discord.Embed(
                color=Colors.DEFAULT,
                description="Please set an counting channel first!",
            )
            await ctx.send(embed=embed)
            await ctx.send_help(self.counting)
            return

        channel = ctx.guild.get_channel(counting.counting_channel)

        embed = discord.Embed(
            title=f"Counting stats for {ctx.guild}:",
            colour=Colors.SUCCESS,
            timestamp=ctx.message.created_at,
        )

        embed.add_field(name="Enabled", value=counting.enabled, inline=False)
        embed.add_field(name="Channel", value=channel.mention, inline=False)
        embed.add_field(name="Goal", value=counting.counting_goal, inline=False)
        embed.add_field(name="Current", value=counting.counting_number, inline=False)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}")

        await ctx.send(embed=embed)

    @counting.command(
        name="toggle",
        description="Toggle Counting On/Off",
        extras={"Examples": "counting toggle True\ncounting toggle False"},
    )
    async def counting_toggle(
        self, ctx: commands.Context, toggle: Optional[bool]
    ) -> None:

        if toggle is None:
            await ctx.send_help(ctx.command)
            return

        guild = await Guild.from_context(ctx)

        if await Counting.exists(guild=guild):
            await Counting.get(guild=guild).update(enabled=toggle)
            if toggle:
                embed = discord.Embed(
                    description=f"Counting has been `enabled`!",
                    color=Colors.DEFAULT,
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=f"Counting has been `disabled`!",
                    color=Colors.DEFAULT,
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description="Please select an counting channel first!",
                color=Colors.ERROR,
            )
            await ctx.send(embed=embed)
            await ctx.send_help(self.counting)

    @counting.command(
        name="channel",
        description="Set The Channel Counting Will Happen In",
        extras={"Examples": "counting channel #counting"},
    )
    async def counting_channel(
        self, ctx: commands.Context, channel: discord.TextChannel
    ) -> None:

        guild = await Guild.from_context(ctx)

        counting, created_new = await Counting.get_or_create(guild=guild)

        if not created_new:
            old_channel: discord.TextChannel = ctx.guild.get_channel(
                counting.counting_channel
            )
            webhooks = await old_channel.webhooks()
            old_hook = discord.utils.get(webhooks, url=counting.webhook_url)
            await old_hook.delete()

        counting.counting_number = 0
        counting.counting_channel = channel.id
        counting.last_member_id = None
        counting.webhook_url = (
            await channel.create_webhook(
                name="Counting", reason="Counting channel webhook"
            )
        ).url
        await counting.save(
            update_fields=[
                "counting_number",
                "counting_channel",
                "webhook_url",
                "last_member_id",
            ]
        )

        embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"Counting channel set to {channel.mention}",
        )
        await ctx.send(embed=embed)

    @counting.command(
        name="goal",
        description="Set A Goal For Counting",
        extras={"Examples": "counting goal 5000"},
    )
    async def counting_goal(self, ctx: commands.Context, goal: int = None) -> None:

        if not goal:
            embed = discord.Embed(
                description="Please specify the goal you want!",
                color=Colors.DEFAULT,
            )
            await ctx.send(embed=embed)
            return

        guild = await Guild.from_context(ctx)

        if await Counting.exists(guild=guild):
            await Counting.get(guild=guild).update(counting_goal=goal)
            embed = discord.Embed(
                description=f"Counting goal set to `{goal}`",
                color=Colors.DEFAULT,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=Colors.DEFAULT,
                description="Please select a Counting Channel First!",
            )
            await ctx.send(embed=embed)
            await ctx.send_help(self.counting)

    @counting.command(
        name="start",
        description="Start Counting From A Number",
        extras={"Examples": "counting start 69\ncounting start 420"},
    )
    async def counting_start(self, ctx, counting_number: int = None) -> None:

        if not counting_number:
            counting_number = 0

        guild = await Guild.from_context(ctx)

        if await Counting.exists(guild=guild):

            await Counting.get(guild=guild).update(counting_number=counting_number)
            embed = discord.Embed(
                description=f"Counting has started from base of `{counting_number}`.",
                color=Colors.DEFAULT,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description="Please select counting channel first!",
                color=Colors.DEFAULT,
            )
            await ctx.send(embed=embed)
            await ctx.send_help(self.counting_channel)

    @counting.command(
        name="reset",
        description="Reset Counting Back To 0",
        extras={"Examples": "counting 0"},
    )
    async def counting_reset(self, ctx):

        guild = await Guild.from_context(ctx)
        exists = await Counting.exists(guild=guild)

        if exists:
            await Counting.get(guild=guild).update(
                counting_number=0, last_member_id=None
            )
            embed = discord.Embed(
                description="Counting Number reset!", color=Colors.DEFAULT
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description="Please select counting channel first!",
                color=Colors.DEFAULT,
            )
            await ctx.send(embed=embed)
            await ctx.send_help(self.counting_channel)

    @commands.is_owner()
    @counting.command(
        name="warnmsg",
        description="Set The Message That Will Send When Someone Messes Up",
        extras={"Examples": "counting warnmsg That Number Is Not Correct"},
    )
    async def counting_warnmsg(self, ctx, *, counting_warn_message: str):
        guild = await Guild.from_context(ctx)

        counting, created_new = await Counting.get_or_create(guild=guild)

        if not created_new:
            counting.counting_warn_message = counting_warn_message
            await counting.save(update_fields=["counting_warn_message"])
            embed = discord.Embed(
                description=f"Counting warn message set to `{counting_warn_message}`",
                color=Colors.DEFAULT,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description="Please select counting channel first!",
                color=Colors.DEFAULT,
            )
            await ctx.send(embed=embed)
            await ctx.send_help(self.counting_channel)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.guild:
            return

        counting = await Counting.get_or_none(guild__discord_id=message.guild.id)

        if not counting:
            return

        if message.channel.id != counting.counting_channel:
            return

        if not message.webhook_id:
            await message.delete()

        if not counting.enabled:
            return
        if message.author.bot:
            return

        if counting.last_member_id == message.author.id:
            await message.author.send(
                f"you can't count twice in a row in {message.channel.mention} of server **{message.guild}**!"
            )
            return

        try:
            sent_number = int(message.content)
        except ValueError:
            await message.author.send(counting.counting_warn_message)
            return

        if sent_number == counting.next_number:
            await counting.increment()
            counting.last_member_id = message.author.id
            await counting.save(update_fields=["last_member_id", "counting_number"])

            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(
                    counting.webhook_url,
                    adapter=discord.AsyncWebhookAdapter(session),
                )

                await webhook.send(
                    message.content,
                    avatar_url=message.author.avatar.url,
                    username=message.author.display_name,
                )
        else:
            await message.author.send(
                f"The number you wrote in {message.channel.mention} of server **{message.guild}** is not valid!"
            )


def setup(bot):
    bot.add_cog(CountingCog(bot))
