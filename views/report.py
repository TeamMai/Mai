import discord
from discord import Embed, SelectOption

from helpers.constants import *
from helpers.types import MEMBER, USER


class UserModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(label="Member ID", placeholder="12345678910")
        )

        self.add_item(
            discord.ui.InputText(
                label="Report Text",
                placeholder="I'm Reporting This User For Being Naughty",
                style=discord.InputTextStyle.long,
            )
        )

        self.add_item(
            discord.ui.InputText(
                label="Evidence",
                placeholder="List Of Screenshots",
                style=discord.InputTextStyle.long,
            )
        )

    async def callback(self, interaction: discord.Interaction) -> None:

        # -- Logging Embed
        embed: Embed = discord.Embed(
            title=f"{Emoji.REPORT} Report Results",
            color=discord.Color.random(),
            description=f"{Emoji.WHITE_CHECKMARK} {interaction.user} **Just Reported A Member!**",
        )
        interaction_user: USER | MEMBER | None = interaction.user
        embed.set_author(
            name=interaction_user.name, icon_url=interaction_user.avatar.url
        )
        embed.set_footer(text=f"User ID: {interaction_user.id}")
        embed.add_field(
            name=f"{Emoji.MEMBERS} Member ID",
            value=self.children[0].value,
            inline=False,
        )
        embed.add_field(
            name=f"{Emoji.REPORT} Report Text",
            value=self.children[1].value,
            inline=False,
        )
        embed.add_field(
            name=f"{Emoji.LINK} EVIDENCE",
            value=self.children[2].value,
            inline=False,
        )
        channel = interaction.client.get_channel(Mai.REPORT_CHANNEL_ID)
        await channel.send(
            content=f"<@&{Mai.STAFF_ROLE_ID}> **New Report Received!**",
            embeds=[embed],
        )

        # -- User Embed

        embed: Embed = discord.Embed(
            color=Colors.SUCCESS,
            description=f"{Emoji.WHITE_CHECKMARK} Report Successfully Sent!",
        )
        await interaction.response.send_message(embeds=[embed])


class GuildModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Guild ID", placeholder="12345678910"))

        self.add_item(
            discord.ui.InputText(
                label="Report Text",
                placeholder="I'm Reporting This User For Being Naughty",
                style=discord.InputTextStyle.long,
            )
        )

        self.add_item(
            discord.ui.InputText(
                label="Evidence",
                placeholder="List Of Screenshots",
                style=discord.InputTextStyle.long,
            )
        )

    async def callback(self, interaction: discord.Interaction) -> None:

        # -- Logging Embed
        embed: Embed = discord.Embed(
            title=f"{Emoji.REPORT} Report Results",
            color=discord.Color.random(),
            description=f"{Emoji.WHITE_CHECKMARK} {interaction.user} **Just Reported A Guild!**",
        )
        interaction_user: USER | MEMBER | None = interaction.user
        embed.set_author(
            name=interaction_user.name, icon_url=interaction_user.avatar.url
        )
        embed.set_footer(text=f"User ID: {interaction_user.id}")
        embed.add_field(
            name=f"{Emoji.MEMBERS} Guild ID",
            value=self.children[0].value,
            inline=False,
        )
        embed.add_field(
            name=f"{Emoji.REPORT} Report Text",
            value=self.children[1].value,
            inline=False,
        )
        embed.add_field(
            name=f"{Emoji.LINK} EVIDENCE",
            value=self.children[2].value,
            inline=False,
        )
        channel = interaction.client.get_channel(Mai.REPORT_CHANNEL_ID)
        await channel.send(
            content=f"<@&{Mai.STAFF_ROLE_ID}> **New Report Received!**",
            embeds=[embed],
        )

        # -- User Embed

        embed: Embed = discord.Embed(
            color=Colors.SUCCESS,
            description=f"{Emoji.WHITE_CHECKMARK} Report Successfully Sent!",
        )
        await interaction.response.send_message(embeds=[embed])


class BugModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                label="Current Behavior",
                placeholder="When I do -ping it ...",
                style=discord.InputTextStyle.long,
            )
        )

        self.add_item(
            discord.ui.InputText(
                label="Expected Behavior",
                placeholder="It Should ...",
                style=discord.InputTextStyle.long,
            )
        )

        self.add_item(
            discord.ui.InputText(
                label="Full Command String",
                placeholder="-command arg1 arg2 ....",
            )
        )

        self.add_item(
            discord.ui.InputText(
                label="Additional Information",
                placeholder="Screenshots, Bot Version, Shard...",
                style=discord.InputTextStyle.long,
            )
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        # -- Logging Embed
        embed: Embed = discord.Embed(
            title=f"{Emoji.REPORT} Report Results",
            color=discord.Color.random(),
            description=f"{Emoji.WHITE_CHECKMARK} {interaction.user} **Just Reported A Bug!**",
        )
        interaction_user: USER | MEMBER | None = interaction.user
        embed.set_author(
            name=interaction_user.name, icon_url=interaction_user.avatar.url
        )
        embed.set_footer(text=f"User ID: {interaction_user.id}")
        embed.add_field(
            name=f"{Emoji.REPORT} Current Behavior",
            value=self.children[0].value,
            inline=False,
        )
        embed.add_field(
            name=f"{Emoji.REPORT} Expected Behavior",
            value=self.children[1].value,
            inline=False,
        )
        embed.add_field(
            name=f"{Emoji.REPORT} Full Command String",
            value=self.children[2].value,
            inline=False,
        )
        embed.add_field(
            name=f"{Emoji.LINK} Additional Information",
            value=self.children[3].value,
            inline=False,
        )
        channel = interaction.client.get_channel(Mai.REPORT_CHANNEL_ID)
        await channel.send(
            content=f"<@&{Mai.DEVELOPER_ROLE_ID}> **New Report Received!**",
            embeds=[embed],
        )

        # -- User Embed

        embed: Embed = discord.Embed(
            color=Colors.SUCCESS,
            description=f"{Emoji.WHITE_CHECKMARK} Report Successfully Sent!",
        )
        await interaction.response.send_message(embeds=[embed])


class Dropdown(discord.ui.Select):
    def __init__(self, bot) -> None:
        self.bot = bot

        options: list[SelectOption] = [
            discord.SelectOption(
                label="User",
                description="You are reporting a User.",
                emoji=Emoji.MEMBERS,
            ),
            discord.SelectOption(
                label="Guild",
                description="You are reporting a Guild.",
                emoji=Emoji.STATS,
            ),
            discord.SelectOption(
                label="Bug",
                description="You are reporting a Bug.",
                emoji=Emoji.REPORT,
            ),
        ]

        super().__init__(
            placeholder="Choose what type of report you are making",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction) -> None:

        if self.values[0] == "User":
            await interaction.response.send_modal(UserModal(title="USER"))
        elif self.values[0] == "Guild":
            await interaction.response.send_modal(GuildModal(title="GUILD"))
        elif self.values[0] == "Bug":
            await interaction.response.send_modal(BugModal(title="BUG"))
        else:
            await interaction.response.send_message(f"{Emoji.ERROR} Error Occurred")


class ReportDropdown(discord.ui.View):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(self.bot))
