"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

from config.ext.parser import config

TORTOISE_CONFIG = {
    "connections": {"default": config["DATABASE_URI"]},
    "apps": {
        config["TORTOISE_APP_NAME"]: {
            "models": [config["DATABASE_MODEL_PATH"], "aerich.models"],
            "default_connection": "default",
        }
    },
    "use_tz": config["DATABASE_USE_TZ"],
    "timezone": config["DATABASE_TIMEZONE"],
}
