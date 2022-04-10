"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import os

import yaml

from helpers.logging import log

ROOT_DIR = os.path.abspath(os.curdir)

CONFIG_PATH = "config/config.yaml"

if not os.path.exists(CONFIG_PATH):
    log.error(
        "[CONFIG] CONFIG.YAML DOES NOT EXIST. PLEASE SEE => config/example.config.yaml"
    )
    raise SystemExit  # Realistically this won't ever be called if you run the launcher but just incase you actually did 'python mai.py' :cringe:

with open(CONFIG_PATH) as f:
    config = yaml.load(f, yaml.Loader)
