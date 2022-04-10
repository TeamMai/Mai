"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import logging

from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="[MAI] %(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
    handlers=[
        RichHandler(
            rich_tracebacks=True,
            omit_repeated_times=False,
            show_path=False,
            show_time=True,
            markup=True,
        ),
    ],
)


log = logging.getLogger("rich")
