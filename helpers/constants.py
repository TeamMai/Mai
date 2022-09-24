"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

from typing import Dict, Final, List, Tuple, final

# -- COLORS


@final
class Colors:

    DEFAULT: Final[int] = 0x4620F1
    SUCCESS: Final[int] = 0x31D85B
    ERROR: Final[int] = 0xFF0000


@final
class Char:
    ARROW: Final[str] = "▸"
    STAR: Final[str] = "★"


# -- LINKS
@final
class Links:

    BOT_AVATAR_URL: Final[
        str
    ] = "https://cdn.discordapp.com/avatars/770898395664875541/c04edaafef86e4efdff7208204e043a6.png?size=2048"
    BOT_INVITE_URL: Final[
        str
    ] = "https://discord.com/api/oauth2/authorize?client_id=889692835329216552&permissions=8&scope=bot%20applications.commands"
    BOT_SOURCE_CODE_URL: Final[str] = "https://github.com/xFGhoul/Mai"
    SUPPORT_SERVER_INVITE: Final[str] = "https://discord.gg/AZQpDFFtqK"
    BOT_DOCUMENTATION_URL: Final[str] = "https://xfghoul.github.io/Mai/"
    TERMS_OF_SERVICE: Final[
        str
    ] = "https://gist.github.com/xFGhoul/51b5bb0991cb55853dcf5b97da5bff77"
    PRIVACY_POLICY: Final[
        str
    ] = "https://gist.github.com/xFGhoul/390a9f57fa9393f7f0ca62ffc6c68b59"
    NSFW_CHANNEL_REQUIRED: Final[str] = "https://i.imgur.com/oe4iK5i.gif"


# -- EMOJIS
@final
class Emoji:
    CHECKMARK: Final[str] = "<a:checkmark:879815681808412744>"
    WHITE_CHECKMARK: Final[str] = "<a:white_checkmark:880919593873461248>"

    # ANIMATED EMOJIS
    ERROR: Final[str] = "<a:error:879815833101164625>"
    LOADING_CIRCLE: Final[str] = "<a:loading_circle:879816001598943273>"
    LOADING_DOTS: Final[str] = "<a:loading_dots:879815965234311238>"
    QUESTION: Final[str] = "<a:what:891444829668667432>"
    NOTIFICATION: Final[str] = "<a:notification:897869079086514227>"
    TWITCH_ANIMATION: Final[str] = "<a:twitchstreaming:945721261265408070>"
    GIVEAWAY: Final[str] = "<a:giveaway:945751649652191293>"

    # STATIC EMOJIS
    CHANNEL: Final[str] = "<:channel:897868496443158639>"
    DEVELOPER: Final[str] = "<:developer:897867252957839401>"
    PYCORD: Final[str] = "<:pycord:898237436499484792>"
    INFORMATION: Final[str] = "<:information:897868584028635146>"
    MENTION: Final[str] = "<:mention:897868536926588939>"
    DISCORD_OFFICIAL_MODERATOR: Final[str] = "<:moderator:897868949151162368>"
    OWNER: Final[str] = "<:crown:898233157671850085>"
    PYTHON: Final[str] = "<:python:897868997943500820>"
    SLASH_COMMAND: Final[str] = "<:slash_command:897868773468569681>"
    STAGE_CHANNEL: Final[str] = "<:stage:897868727746449538>"
    STATS: Final[str] = "<:stats:897867757209661471>"
    VOICE_CHANNEL: Final[str] = "<:voice_channel:897868449261432892>"
    WINDOWS_10: Final[str] = "<:windows10:898231148029837314>"
    CPU: Final[str] = "<:CPU:898231378125156383>"
    PC: Final[str] = "<:pc:898231801301049394>"
    RAM: Final[str] = "<:RAM:898233910293581845>"
    MAI: Final[str] = "<:mai:898238143004835900>"
    LINK: Final[str] = "<:link:898239182177194024>"
    MEMBERS: Final[str] = "<:members:901917213877997619>"
    MESSAGES: Final[str] = "<:messages:901917529268682752>"
    DISCORD_EMPLOYEE: Final[str] = "<:employee:901918060909326376>"
    BRAIN: Final[str] = "<:BigBrainTime:914164430172983397>"
    REDIS: Final[str] = "<:redis:919271191569637426>"
    DISCORD: Final[str] = "<:discord:919271214097235978>"
    POSTGRESQL: Final[str] = "<:postgresql:919271276265226290>"
    YOUTUBE: Final[str] = "<:youtube:938807020059000842>"
    SPOTIFY: Final[str] = "<:spotify:938804909913018438>"
    SOUNDCLOUD: Final[str] = "<:soundcloud:938804829659222036>"
    TWITTER: Final[str] = "<:twitter:945720710783971338>"
    INSTAGRAM: Final[str] = "<:instagram:945720858268291182>"
    TWITCH: Final[str] = "<:twitch:945721231603281970>"
    TIKTOK: Final[str] = "<:tiktok:945721504597934080>"
    GENSHIN_IMPACT: Final[str] = "<:genshinimpact:945747628891725834>"
    ANILIST: Final[str] = "<:Anilist:945747535807529021>"
    MY_ANIME_LIST: Final[str] = "<:MyAnimeList:945747485291319397>"
    ECONOMY: Final[str] = "<:economy:945747383092912188>"
    AFK: Final[str] = "<:AFK:945747339212128287>"
    SNIPER: Final[str] = "<:sniper:945728578677506128>"
    TAG: Final[str] = "<:tag:945728326000066600>"
    POLLS: Final[str] = "<:polls:945729635105251388>"
    ROBLOX: Final[str] = "<:roblox:945729388333383690>"
    OSU: Final[str] = "<:osu:945730029827031102>"
    MINECRAFT: Final[str] = "<:minecraft:945731420880535652>"
    MUSIC: Final[str] = "<:music:945730564978245682>"
    NSFW: Final[str] = "<:nsfwchannel:945730258332680223>"
    LEVELING: Final[str] = "<:leveling:945750872992923738>"
    IMAGE: Final[str] = "<:image:945751323272437800>"
    COUNTING: Final[str] = "<:counting:945752433005588552>"
    CAPTCHA: Final[str] = "<:captcha:945752861290139759>"
    COD: Final[str] = "<:CoD:945752936888287253>"
    TOPGG: Final[str] = "<:topgg:945754227102351400>"
    STATCORD: Final[str] = "<:statcord:945754289521963079>"
    CHANGELOGS: Final[str] = "<:changelogs:945754392190132245>"
    REPORT: Final[str] = "<:CH_BadgeBugHunter:795849415993720832>"
    VALORANT: Final[str] = "<:valorant:957331465174147112>"


# -- OSU EMOJIS

# NOTE: THANKS owo bot :)


@final
class OsuEmotes:

    SS: Final[str] = "<:SS_rank:893221340071473203>"
    SSHD: Final[str] = "<:SSHD_rank:893221226397433897>"
    SHD: Final[str] = "<:SHD_rank:893221280382341174>"
    S: Final[str] = "<:S_rank:893221182021701722>"
    A: Final[str] = "<:A_rank:893221133472657459>"
    B: Final[str] = "<:B_rank:893584405614981170>"
    C: Final[str] = "<:C_rank:893584447029522433>"
    D: Final[str] = "<:D_rank:893584464997920818>"
    F: Final[str] = "<:F_rank:893584427832213584>"

    # OSU LINKS

    OSU_LOGO_IMAGE: Final[str] = "https://i.imgur.com/Req9wGs.png"


@final
class ConfigMapping:
    YAML: Final[Dict] = {
        "DISCORD_TOKEN": "",
        "DISCORD_ID": "",
        "DATABASE_URI": "",
        "DATABASE_MODEL_PATH": "",
        "DATABASE_TIMEZONE": "",
        "DATABASE_USE_TZ": "",
        "USE_DOCKER": "",
        "BOT_NAME": "",
        "BOT_OWNERS": "",
        "SERVER_BLACKLIST_CHANNEL_ID": "",
        "RUN_LAUNCHER_WITH_EXTRA_SYS_INFO": "",
        "DEFAULT_REDIS_PATH": "",
        "REDIS_URI": "",
        "OSU_API_V1_KEY": "",
        "OSU_API_V2_CLIENT_ID": "",
        "OSU_API_V2_CLIENT_SECRET": "",
        "OSU_API_V2_CLIENT_CALLBACK_URL": "",
        "BITLY_API_TOKEN": "",
        "DEFAULT_PREFIX": "",
        "BOT_VERSION": "",
        "BOT_LOGS_CHANNEL_ID": "",
        "RPC_ENABLED": "",
        "RPC_LARGE_IMAGE": "",
        "RPC_LARGE_TEXT": "",
        "RPC_SMALL_IMAGE": "",
        "RPC_SMALL_TEXT": "",
        "PRAW_ID": "",
        "PRAW_SECRET": "",
        "YOUTUBE_API_KEY": "",
        "SPOTIFY_CLIENT_ID": "",
        "SPOTIFY_CLIENT_SECRET": "",
        "TWITCH_API_ID": "",
        "TWITCH_API_SECRET": "",
        "X_RAPID_API_KEY": "",
        "X_RAPID_API_HOST": "",
        "SOME_RANDOM_API_KEY": "",
        "STATCORD_API_KEY": "",
        "DAGPI_API_KEY": "",
        "KAWAII_RED_API_TOKEN": "",
        "GENIUS_API_TOKEN": "",
        "API_FLASH_TOKEN": "",
        "AZREAL_API_TOKEN": "",
    }


@final
class ValidTypes:
    Logging: Final[List] = [
        "channel_created",
        "channel_deleted",
        "channel_updated",
        "member_banned",
        "member_joined",
        "member_joined_voice_channel",
        "member_left",
        "member_left_voice_channel",
        "member_roles_changed",
        "member_unbanned",
        "member_updated",
        "message_deleted",
        "message_edited",
        "nickname_changed",
        "role_created",
        "role_deleted",
        "role_updated",
        "server_edited",
        "server_emojis_updated",
        "server_stickers_updated",
        "server_webhooks_updated",
        "invite_created",
        "invite_deleted",
        "stage_created",
        "stage_deleted",
        "stage_updated",
        "warn_created",
        "warn_deleted",
    ]


@final
class Limitations:
    MAX_WARNING_REASON: Final[int] = 350

    ALLOWED_FILE_EXTENSIONS: Final[Tuple] = (".gif", ".png", ".jpg", ".jpeg")

    class Discord:
        MAX_MESSAGE_SIZE: Final[int] = 2000
        MAX_CHANNELS: Final[int] = 500
        MAX_CHANNELS_PER_CATEGORY: Final[int] = 10
        MAX_ROLES: Final[int] = 250
        MAX_PINNED_MESSAGES: Final[int] = 50
        MAX_NICKNAME_LENGTH: Final[int] = 32
        MAX_TOPIC_LENGTH: Final[int] = 1024

        class NitroUser:
            MAX_MESSAGE_SIZE: Final[int] = 4000

        class Embed:
            MAX_FIELD_SIZE: Final[int] = 25
            MAX_TITLE: Final[int] = 256
            MAX_FIELD_NAME: Final[int] = 256
            MAX_FIELD_VALUE: Final[int] = 1024
            MAX_FOOTER_SIZE: Final[int] = 4096
            MAX_DESCRIPTION_SIZE: Final[int] = 4096


@final
class Mai:
    SUPPORT_SERVER_ID: Final[int] = 889542746027741194
    GHOUL_DISCORD_ID: Final[int] = 433026067050266634
    NERD_DISCORD_ID: Final[int] = 186202944461471745

    SUPPORT_SERVER_BAN_APPEAL: Final[
        str
    ] = "https://docs.google.com/forms/d/e/1FAIpQLSe3-YwwlFPiWecKL73Y8YQyFHlrgThHfy544okQ7hD34b3kQw/viewform"
    USER_BAN_APPEAL: Final[
        str
    ] = "https://docs.google.com/forms/d/e/1FAIpQLSdI-NW2dtvLx5s7JIInGtUnhGw5Hqbfrl1Xdw_VNYLWWWohAg/viewform"
    GUILD_BAN_APPEAL: Final[
        str
    ] = "https://docs.google.com/forms/d/e/1FAIpQLSfaW0A8LnzWCmQblkwS_uve_grnYz97ZJQIw9BkeUpLQB27xg/viewform"

    REPORT_CHANNEL_ID: Final[int] = 955258448981942322

    STAFF_ROLE_ID: Final[int] = 889542746027741201
    DEVELOPER_ROLE_ID: Final[int] = 889542746027741203

    DEVELOPER_FOOTER: Final[str] = "Made With ❤️ By Ghoul & Nerd"
