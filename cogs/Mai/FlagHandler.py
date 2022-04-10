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
import datetime


from discord.ext import commands

from helpers.constants import *
from helpers.logging import log

from db.models import Guild

from config.ext.parser import config


class FlagHandler(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.spam_control = commands.CooldownMapping.from_cooldown(
            10, 10, commands.BucketType.user
        )

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        guild = await Guild.c_get_or_none_by_discord_id(message.guild.id)

        if guild.is_bot_blacklisted:
            return

        if not message.guild:
            return

        if message.author.bot:
            return

        context = await self.bot.get_context(message)

        if context.valid:
            bucket = self.spam_control.get_bucket(message)
            retry_after = bucket.update_rate_limit()

            if retry_after:
                try:
                    flag_spamming_channel = self.bot.get_channel(
                        config["BOT_LOGS_CHANNEL_ID"]
                    )

                    embed = discord.Embed(
                        color=Colors.DEFAULT,
                        title="Command Spam Warning",
                        description=f"**{self.bot.user.name} has Automatically Flagged {message.author.mention} for spamming more than `{bucket.rate}` commands in `{bucket.per}` seconds**\n**Here is the list of data:**",
                        timestamp=datetime.datetime.utcnow(),
                    )
                    embed.set_author(
                        name=message.author.name,
                        icon_url=message.author.avatar.url,
                    )
                    embed.set_thumbnail(url=message.author.avatar.url)
                    embed.add_field(
                        name="User Name", value=f"`{message.author}`"
                    )
                    embed.add_field(
                        name="User ID", value=f"`{message.author.id}`"
                    )
                    embed.add_field(
                        name="Channel Name", value=f"`{message.channel}`"
                    )
                    embed.add_field(
                        name="Channel ID", value=f"`{message.channel.id}`"
                    )
                    await flag_spamming_channel.send(embed=embed)

                    user_warn_embed = discord.Embed(
                        color=Colors.ERROR,
                        description=f" {Emoji.ERROR} {message.author.mention}, You Are Using Commands Too Fast!",
                    )
                    await message.channel.send(embed=user_warn_embed)
                    return
                except Exception as e:
                    log.exception(type(e), e)
        else:
            return


def setup(bot):
    bot.add_cog(FlagHandler(bot))
