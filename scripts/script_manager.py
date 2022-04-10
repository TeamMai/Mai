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
import subprocess
import sys

from helpers.console import console
from InquirerPy import inquirer

WINDOW_TITLE = "[Mai] - Script Manager"

clear_console = "cls" if sys.platform == "win32" else "clear"

os.system(f"{clear_console} && title {WINDOW_TITLE}")


console.print(
    """[blue3]

    ███████╗ ██████╗██████╗ ██╗██████╗ ████████╗    ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗
    ██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝    ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗
    ███████╗██║     ██████╔╝██║██████╔╝   ██║       ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝
    ╚════██║██║     ██╔══██╗██║██╔═══╝    ██║       ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗
    ███████║╚██████╗██║  ██║██║██║        ██║       ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║
    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝       ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝

[/blue3]""",
    justify="full",
)


console.print(
    f"\n[blue3]WELCOME TO THE MAI SCRIPT MANAGER [purple]{os.getlogin()}[/purple][/blue3]\n\n"
)

console.print(
    "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]"
)


terminal = inquirer.select(
    message="Which Terminal Are You On?", choices=["CMD/Powershell", "Bash"]
).execute()

if terminal == "CMD/Powershell":

    print("\n")

    script = inquirer.select(
        message="What Script Would You Like To Execute?",
        choices=[
            "build_database",
            "rebuild_database",
            "upgrade_database",
        ],
    ).execute()

    console.print(
        f"[blue3]> [red]{script}.bat[/red] Was Chosen, Executing...[/blue3]"
    )

    ROOT_DIR = os.path.abspath(os.curdir)

    WIN32_DIR = "win32"

    WINDOWS_SCRIPTS_DIR = os.path.join(ROOT_DIR, WIN32_DIR)

    subprocess.Popen([script], cwd=WINDOWS_SCRIPTS_DIR, shell=True)

elif terminal == "Bash":

    print("\n")

    script = inquirer.select(
        message="What Script Would You Like To Execute?",
        choices=[
            "build_database",
            "rebuild_database",
            "upgrade_database",
        ],
    ).execute()

    console.print(
        f"\n[blue3]> [red]{script}.bat[/red] Was Chosen, Executing...[/blue3]"
    )

    ROOT_DIR = os.path.abspath(os.curdir)

    LINUX_DIR = "linux"

    BASH_SCRIPTS_DIR = os.path.join(ROOT_DIR, LINUX_DIR)

    subprocess.Popen([f"./{script}.sh"], cwd=BASH_SCRIPTS_DIR, shell=True)
else:
    console.print("[red]> Wrong Input Provided, Try Again.[/red]")
