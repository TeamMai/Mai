"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

# -- COLORS
class Colors:

    DEFAULT = 0x4620F1
    SUCCESS = 0x31D85B
    ERROR = 0xFF0000


class Chars:
    ARROW = "▸"


# -- LINKS
class Links:

    BOT_AVATAR_URL = "https://cdn.discordapp.com/avatars/770898395664875541/c04edaafef86e4efdff7208204e043a6.png?size=2048"
    BOT_INVITE_URL = "https://discord.com/api/oauth2/authorize?client_id=889692835329216552&permissions=536870911991&scope=bot"
    BOT_SOURCE_CODE_URL = "https://github.com/xFGhoul/Mai"
    SUPPORT_SERVER_INVITE = "https://discord.gg/AZQpDFFtqK"
    BOT_DOCUMENTATION_URL = "https://xfghoul.github.io/Mai/"
    TERMS_OF_SERVICE = (
        "https://gist.github.com/xFGhoul/51b5bb0991cb55853dcf5b97da5bff77"
    )
    PRIVACY_POLICY = (
        "https://gist.github.com/xFGhoul/390a9f57fa9393f7f0ca62ffc6c68b59"
    )
    NSFW_CHANNEL_REQUIRED = "https://i.imgur.com/oe4iK5i.gif"


# -- EMOJIS
class Emoji:
    CHECKMARK = "<a:checkmark:879815681808412744>"
    WHITE_CHECKMARK = "<a:white_checkmark:880919593873461248>"

    # ANIMATED EMOJIS
    ERROR = "<a:error:879815833101164625>"
    LOADING_CIRCLE = "<a:loading_circle:879816001598943273>"
    LOADING_DOTS = "<a:loading_dots:879815965234311238>"
    QUESTION = "<a:what:891444829668667432>"
    NOTIFICATION = "<a:notification:897869079086514227>"
    TWITCH_ANIMATION = "<a:twitchstreaming:945721261265408070>"
    GIVEAWAY = "<a:giveaway:945751649652191293>"

    # STATIC EMOJIS
    CHANNEL = "<:channel:897868496443158639>"
    DEVELOPER = "<:developer:897867252957839401>"
    PYCORD = "<:pycord:898237436499484792>"
    INFORMATION = "<:information:897868584028635146>"
    MENTION = "<:mention:897868536926588939>"
    DISCORD_OFFICIAL_MODERATOR = "<:moderator:897868949151162368>"
    OWNER = "<:crown:898233157671850085>"
    PYTHON = "<:python:897868997943500820>"
    SLASH_COMMAND = "<:slash_command:897868773468569681>"
    STAGE_CHANNEL = "<:stage:897868727746449538>"
    STATS = "<:stats:897867757209661471>"
    VOICE_CHANNEL = "<:voice_channel:897868449261432892>"
    WINDOWS_10 = "<:windows10:898231148029837314>"
    CPU = "<:CPU:898231378125156383>"
    PC = "<:pc:898231801301049394>"
    RAM = "<:RAM:898233910293581845>"
    MAI = "<:mai:898238143004835900>"
    LINK = "<:link:898239182177194024>"
    MEMBERS = "<:members:901917213877997619>"
    MESSAGES = "<:messages:901917529268682752>"
    DISCORD_EMPLOYEE = "<:employee:901918060909326376>"
    BRAIN = "<:BigBrainTime:914164430172983397>"
    REDIS = "<:redis:919271191569637426>"
    DISCORD = "<:discord:919271214097235978>"
    POSTGRESQL = "<:postgresql:919271276265226290>"
    YOUTUBE = "<:youtube:938807020059000842>"
    SPOTIFY = "<:spotify:938804909913018438>"
    SOUNDCLOUD = "<:soundcloud:938804829659222036>"
    TWITTER = "<:twitter:945720710783971338>"
    INSTAGRAM = "<:instagram:945720858268291182>"
    TWITCH = "<:twitch:945721231603281970>"
    TIKTOK = "<:tiktok:945721504597934080>"
    GENSHIN_IMPACT = "<:genshinimpact:945747628891725834>"
    ANILIST = "<:Anilist:945747535807529021>"
    MY_ANIME_LIST = "<:MyAnimeList:945747485291319397>"
    ECONOMY = "<:economy:945747383092912188>"
    AFK = "<:AFK:945747339212128287>"
    SNIPER = "<:sniper:945728578677506128>"
    TAG = "<:tag:945728326000066600>"
    POLLS = "<:polls:945729635105251388>"
    ROBLOX = "<:roblox:945729388333383690>"
    OSU = "<:osu:945730029827031102>"
    MINECRAFT = "<:minecraft:945731420880535652>"
    MUSIC = "<:music:945730564978245682>"
    NSFW = "<:nsfwchannel:945730258332680223>"
    LEVELING = "<:leveling:945750872992923738>"
    IMAGE = "<:image:945751323272437800>"
    COUNTING = "<:counting:945752433005588552>"
    CAPTCHA = "<:captcha:945752861290139759>"
    COD = "<:CoD:945752936888287253>"
    TOPGG = "<:topgg:945754227102351400>"
    STATCORD = "<:statcord:945754289521963079>"
    CHANGELOGS = "<:changelogs:945754392190132245>"
    REPORT = "<:CH_BadgeBugHunter:795849415993720832>"
    VALORANT = "<:valorant:957331465174147112>"


# -- OSU EMOJIS

# NOTE: THANKS owo bot :)


class OsuEmotes:

    SS = "<:SS_rank:893221340071473203>"
    SSHD = "<:SSHD_rank:893221226397433897>"
    SHD = "<:SHD_rank:893221280382341174>"
    S = "<:S_rank:893221182021701722>"
    A = "<:A_rank:893221133472657459>"
    B = "<:B_rank:893584405614981170>"
    C = "<:C_rank:893584447029522433>"
    D = "<:D_rank:893584464997920818>"
    F = "<:F_rank:893584427832213584>"

    # OSU LINKS

    OSU_LOGO_IMAGE = "https://i.imgur.com/Req9wGs.png"
    STAR_ICON = "★"


class ConfigMapping:
    YAML = {
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


class ValidTypes:
    Logging = {
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
    }


class Limitations:
    MAX_WARNING_REASON = 350

    class Discord:
        MAX_MESSAGE_SIZE = 2000
        MAX_CHANNELS = 500
        MAX_CHANNELS_PER_CATEGORY = 10
        MAX_ROLES = 250
        MAX_PINNED_MESSAGES = 50
        MAX_NICKNAME_LENGTH = 32
        MAX_TOPIC_LENGTH = 1024

        class NitroUser:
            MAX_MESSAGE_SIZE = 4000

        class Embed:
            MAX_FIELD_SIZE = 25
            MAX_TITLE = 256
            MAX_FIELD_NAME = 256
            MAX_FIELD_VALUE = 1024
            MAX_FOOTER_SIZE = 4096
            MAX_DESCRIPTION_SIZE = 4096


class Mai:
    SUPPORT_SERVER_ID = 889542746027741194
    GHOUL_DISCORD_ID = 433026067050266634
    NERD_DISCORD_ID = 186202944461471745

    SUPPORT_SERVER_BAN_APPEAL = "https://docs.google.com/forms/d/e/1FAIpQLSe3-YwwlFPiWecKL73Y8YQyFHlrgThHfy544okQ7hD34b3kQw/viewform"
    USER_BAN_APPEAL = "https://docs.google.com/forms/d/e/1FAIpQLSdI-NW2dtvLx5s7JIInGtUnhGw5Hqbfrl1Xdw_VNYLWWWohAg/viewform"
    GUILD_BAN_APPEAL = "https://docs.google.com/forms/d/e/1FAIpQLSfaW0A8LnzWCmQblkwS_uve_grnYz97ZJQIw9BkeUpLQB27xg/viewform"

    REPORT_CHANNEL_ID = 955258448981942322

    STAFF_ROLE_ID = 889542746027741201
    DEVELOPER_ROLE_ID = 889542746027741203
