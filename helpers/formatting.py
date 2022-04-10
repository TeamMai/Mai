"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

from itertools import groupby

from discord import Embed

from db.models import ServerLogging
from .constants import *


def emoji(value: bool) -> str:
    """Convert a boolean value to an emoji

    Parameters
    ----------
    value : bool
        Value to represent

    Returns
    -------
    str
        Either a check mark or cross mark emoji
    """
    return Emoji.CHECKMARK if value else Emoji.ERROR


def format_setting(model: ServerLogging, setting: str) -> str:
    setting_title = (
        f"`{' '.join(setting.split('_')[1:]).replace('_', ' ').title()}`"
    )
    enabled = getattr(model, setting)
    return f"\t{setting_title}: {emoji(enabled)}"


def format_logging_model(model: ServerLogging) -> Embed:
    """Formats logging settings as an embed

    Parameters
    ----------
    model : ServerLogging
        Model retrieved from a database

    Returns
    -------
    Embed
        Embed representing all settings of the logging system
    """
    embed = Embed(color=Colors.DEFAULT)
    grouped = groupby(sorted(ValidTypes.Logging), key=lambda k: k.split("_")[0])
    for group_name, contents in grouped:
        group_title = group_name.title()
        settings = "\n".join(
            [format_setting(model, setting) for setting in contents]
        )
        embed.add_field(name=group_title, value=settings, inline=False)

    return embed
