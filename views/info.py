import discord


from helpers.constants import *


class Invite(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(
            discord.ui.Button(label="Invite the Bot!", url=Links.BOT_INVITE_URL)
        )


class SupportServer(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(
            discord.ui.Button(
                label="Support Server", url=Links.SUPPORT_SERVER_INVITE
            )
        )


class Source(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(
            discord.ui.Button(
                label="View The Source Code",
                url=Links.BOT_SOURCE_CODE_URL,
            )
        )
