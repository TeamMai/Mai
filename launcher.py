"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import datetime
import os
import platform
import subprocess
import sys
import time

import cpuinfo
import humanize
import psutil
import yaml

from download import download
from halo import Halo
from InquirerPy import inquirer


from helpers import ASCII

from config.ext.parser import config

from helpers.console import console
from helpers.constants import ConfigMapping


console.print(
    "[red]-----------------------------------------------------------------[/red"
)
raise DeprecationWarning(
    "[MAI] THIS LAUNCHER IS DEPRECATED AND SHOULD NOT BE USED"
)
console.print(
    "[red]-----------------------------------------------------------------[/red"
)


ascii = ASCII()


def WaitAndExit(message) -> SystemExit:
    time.sleep(2)
    os.system("cls" if sys.platform == "win32" else "clear")
    ascii.error()
    ascii.line()
    console.print(f"[red]{message}[/red]")
    time.sleep(5)
    raise SystemExit


# First System Check

if sys.platform != "win32":
    WaitAndExit("THIS LAUNCHER CAN ONLY BE USED ON WINDOWS")


# Setting Up Some Constants

WINDOW_TITLE = "[Mai] - Launcher"

clear_console = "cls" if sys.platform == "win32" else "clear"

os.system(f"{clear_console} && title {WINDOW_TITLE}")

logo = """[blue3]

                                    ███╗   ███╗ █████╗ ██╗      ██╗██████╗
                                    ████╗ ████║██╔══██╗██║     ██╔╝╚════██╗
                                    ██╔████╔██║███████║██║    ██╔╝  █████╔╝
                                    ██║╚██╔╝██║██╔══██║██║    ╚██╗  ╚═══██╗
                                    ██║ ╚═╝ ██║██║  ██║██║     ╚██╗██████╔╝
                                    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝      ╚═╝╚═════╝

[/blue3]"""


console.print(logo, justify="full")

console.print(
    f"\n[blue3]WELCOME TO THE MAI LAUNCHER[/blue3] [purple]{os.getlogin()}[/purple]\n\n"
)

console.print(
    "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]"
)

boot_time_timestamp = psutil.boot_time()
bt = datetime.datetime.fromtimestamp(boot_time_timestamp)

console.print(
    f"[blue3]Current Path:[/blue3] [purple]{os.path.abspath(os.getcwd())}[/purple]\n"
)

console.print(f"[blue3]OS[/blue3]: [purple]{platform.uname().system}[/purple]")
console.print(
    f"[blue3]OS Version[/blue3]: [purple]{platform.uname().version}[/purple]"
)
console.print(
    f"[blue3]Release[/blue3]: [purple]{platform.uname().release}[/purple]"
)
console.print(
    f"[blue3]Processor[/blue3]: [purple]{platform.uname().processor}[/purple]"
)
console.print(
    f"[blue3]Python Version[/blue3]: [purple]{platform.python_version()}[/purple]"
)
console.print(
    f"[blue3]Boot Time[/blue3]: [purple]{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}[/purple]"
)

console.print(
    "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]"
)

run_extra_sys_info = config["RUN_LAUNCHER_WITH_EXTRA_SYS_INFO"]

if run_extra_sys_info == True:
    cpu_info = cpuinfo.get_cpu_info()

    cpu_name = cpu_info["brand_raw"]
    processor_type = cpu_info["arch"]
    cpu_cores = cpu_info["count"]

    console.print(f"[blue3]CPU[/blue3]: [purple]{cpu_name}[/purple]")
    console.print(
        f"[blue3]Processor Type[/blue3]: [purple]{processor_type}[/purple]"
    )
    console.print(f"[blue3]CPU Cores[/blue3]: [purple]{cpu_cores}[/purple]")
    console.print(
        f"[blue3]CPU Percentage[/blue3]: [purple]{psutil.cpu_percent()}%[/purple]"
    )

    console.print(
        "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]"
    )

    vmem = psutil.virtual_memory()

    console.print(
        f"[blue3]Total Memory[/blue3]: [purple]{humanize.naturalsize(vmem.total)}[/purple]"
    )
    console.print(
        f"[blue3]Available[/blue3]: [purple]{humanize.naturalsize(vmem.available)}[/purple]"
    )
    console.print(f"[blue3]Percent[/blue3]: [purple]{vmem.percent}%[/purple]")
    console.print(
        f"[blue3]Used[/blue3]: [purple]{humanize.naturalsize(vmem.used)}[/purple]"
    )
    console.print(
        f"[blue3]Free[/blue3]: [purple]{humanize.naturalsize(vmem.free)}[/purple]"
    )

    console.print(
        "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]"
    )

    time.sleep(1)


time.sleep(1)

console.print(
    """[blue3]

                                 ██████╗ ██████╗ ███╗   ██╗███████╗██╗ ██████╗
                                ██╔════╝██╔═══██╗████╗  ██║██╔════╝██║██╔════╝
                                ██║     ██║   ██║██╔██╗ ██║█████╗  ██║██║  ███╗
                                ██║     ██║   ██║██║╚██╗██║██╔══╝  ██║██║   ██║
                                ╚██████╗╚██████╔╝██║ ╚████║██║     ██║╚██████╔╝
                                 ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝

[/blue3]""",
    justify="full",
)


console.print(
    "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]"
)

if not os.path.exists("config/config.yaml"):
    console.print("[red]> CONFIG FILE NOT FOUND.[/red]\n")

    time.sleep(1)

    console.print("[blue3]> STARTING CONFIG GENERATOR[/blue3]\n")

    conf = ConfigMapping.YAML

    if (
        str(
            console.input(
                "[blue3]Would You Like To Enter Config Values Now?[/blue3] ",
                markup=True,
            )
        ).lower()
        == "y"
        or "yes"
        or "Y"
        or "Yes"
    ):
        for key in conf.keys():
            conf[key] = console.input(
                f"\n[blue3]Please enter the desired value for key '{key}': [/blue3]",
                markup=True,
            )

    with open("config/config.yaml", "w+") as f:
        console.print("[blue3]> DUMPING CONFIG DATA TO CONFIG.YAML[/blue3]")
        yaml.dump(conf, f, yaml.Dumper)
        console.print("[blue3]> CONFIG DATA DUMPED.[/blue3]")
        time.sleep(1)
else:
    console.print(
        "[blue3]> Config File: [purple]config/config.yaml[/purple][/blue3]"
    )

console.print(
    "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]"
)

# REDIS

console.print(
    """[blue3]

                                        ██████╗ ███████╗██████╗ ██╗███████╗
                                        ██╔══██╗██╔════╝██╔══██╗██║██╔════╝
                                        ██████╔╝█████╗  ██║  ██║██║███████╗
                                        ██╔══██╗██╔══╝  ██║  ██║██║╚════██║
                                        ██║  ██║███████╗██████╔╝██║███████║
                                        ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝╚══════╝

[/blue3]""",
    justify="full",
)

console.print(
    "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]"
)

redis_running = "redis-server.exe" in (p.name() for p in psutil.process_iter())

if not redis_running:

    from config.ext.parser import config

    possible_redis_path = config["DEFAULT_REDIS_PATH"]

    console.print("[red]> REDIS NOT FOUND.[/red]\n")

    if possible_redis_path is None:

        install_redis = inquirer.select(
            message="How Should I Handle Redis?",
            choices=["Custom Path", "Install(And Run) Redis"],
        ).execute()

        if install_redis == "Custom Path":

            redis_path = console.input(
                "[blue3]> Supply An Absolute Path For Redis: [/blue3]",
                markup=True,
            )

            if os.path.exists(redis_path):
                console.print(
                    f"[blue3]> VALIDATED [red]{redis_path}[/red], STARTING...[/blue3]\n\n"
                )
            else:
                WaitAndExit("> Please Return A Valid Path Next Time.")

            console.print(
                f"\n[blue3]Selected Path[/blue3]: [purple]{redis_path}[/purple]\n\n"
            )
            console.print("[blue3]> LAUNCHING REDIS[/blue3]\n")
            subprocess.Popen(
                ["redis-server"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                cwd=redis_path,
                shell=True,
            )
            console.print("[blue3]> REDIS IS RUNNING AND FUNCTIONING[/blue3]\n")

            time.sleep(1)

        elif install_redis == "Install(And Run) Redis":

            redis_path = console.input(
                "[blue3]> Supply An Absolute Path For Redis: [/blue3]",
                markup=True,
            )

            console.print(
                f"\n[blue3]Selected Path[/blue3]: [purple]{redis_path}[/purple]\n\n"
            )
            redis_for_win_url = "https://github.com/microsoftarchive/redis/releases/download/win-3.2.100/Redis-x64-3.2.100.zip"
            console.print(
                f"[blue3]Download URL[/blue3]: [purple]{redis_for_win_url}[/purple]\n\n"
            )
            spinner = Halo(
                text="Downloading Redis",
                color="cyan",
                text_color="cyan",
                spinner="dots",
            )
            spinner.start()
            download(
                redis_for_win_url,
                path=redis_path,
                kind="zip",
                progressbar=False,
                replace=True,
                verbose=False,
            )
            spinner.stop()
            console.print(
                f"\n[blue3]> REDIS HAS BEEN INSTALLED AND EXTRACTED TO[/blue3] [red]{redis_path}[/red].\n"
            )
            time.sleep(1)

            console.print("[blue3]> LAUNCHING REDIS[/blue3]\n")
            subprocess.Popen(
                ["redis-server"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                cwd=redis_path,
                shell=True,
            )
            console.print("[blue3]> REDIS IS RUNNING AND FUNCTIONING[/blue3]\n")
            time.sleep(1)
        else:
            WaitAndExit("> An Unexpected Error Occurred.")
    else:
        console.print(
            "[blue3]> FOUND DEFAULT_REDIS_PATH FROM CONFIG.YAML[/blue3]"
        )
        subprocess.Popen(
            ["redis-server"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            cwd=possible_redis_path,
            shell=True,
        )
        console.print("[blue3]> RUNNING REDIS FROM DEFAULT_REDIS_PATH[/blue3]")
else:
    console.print(
        f"[blue3]Redis Port:[/blue3] [purple]redis://localhost:6379[/purple]"
    )
    console.print(
        f"[blue3]Redis Process:[/blue3] [purple]redis-server.exe[/purple]"
    )

console.print(
    "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]"
)

# FILE CHECKS

console.print(
    """[blue3]

                                ██████╗  ██████╗ ███████╗████████╗██████╗ ██╗   ██╗
                                ██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝██╔══██╗╚██╗ ██╔╝
                                ██████╔╝██║   ██║█████╗     ██║   ██████╔╝ ╚████╔╝
                                ██╔═══╝ ██║   ██║██╔══╝     ██║   ██╔══██╗  ╚██╔╝
                                ██║     ╚██████╔╝███████╗   ██║   ██║  ██║   ██║
                                ╚═╝      ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝

[/blue3]""",
    justify="full",
)


console.print(
    "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]"
)


if not os.path.exists("poetry.lock"):
    time.sleep(1)

    console.print(
        "[red]> POETRY.LOCK NOT FOUND, ASSUMING NO POETRY PACKAGES HAVE BEEN INSTALLED, INSTALLING POETRY...[/red]\n"
    )
    subprocess.call(
        ["pip", "install", "poetry"],
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    console.print(f"[blue3]> POETRY INSTALLED, INSTALLING PACKAGES[/blue3]\n")
    subprocess.call(
        ["poetry", "install"],
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    console.print(f"[blue3]> INSTALLED POETRY PACKAGES.[/blue3]\n")
    time.sleep(2)
else:
    console.print(
        f"[blue3]> Poetry Lock File: [purple]poetry.lock[purple][/blue3]"
    )
    console.print(
        f"[blue3]> Poetry Toml File: [purple]pyproject.toml[purple][/blue3]"
    )

console.print(
    "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]"
)

console.print(
    """[blue3]

                        ██████╗  █████╗ ████████╗ █████╗ ██████╗  █████╗ ███████╗███████╗
                        ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝
                        ██║  ██║███████║   ██║   ███████║██████╔╝███████║███████╗█████╗
                        ██║  ██║██╔══██║   ██║   ██╔══██║██╔══██╗██╔══██║╚════██║██╔══╝
                        ██████╔╝██║  ██║   ██║   ██║  ██║██████╔╝██║  ██║███████║███████╗
                        ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝

[/blue3]""",
    justify="full",
)

console.print(
    "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]"
)

if not os.path.exists("aerich.ini"):
    console.print("[red]> DATABASE DATA NOT FOUND[/red]\n")
    time.sleep(1)

    console.print("[blue3]BUILDING DATABASE WITH CONFIG DATA.[/blue3]\n")

    terminal = inquirer.select(
        message="Which Terminal Are You On?", choices=["CMD/Powershell", "Bash"]
    ).execute()

    cd_path = "scripts/win32" if terminal == "CMD/Powershell" else "linux"

    build_database_command = (
        "build_database"
        if terminal == "CMD/Powershell"
        else "./build_database.sh"
    )

    subprocess.call(
        [build_database_command],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        cwd=cd_path,
        shell=True,
    )
    console.print("[blue3]> DATABASE BUILT WITH CONFIG DATA.[/blue3]")
    time.sleep(2)
else:
    console.print("[blue3]Aerich Config: [purple]aerich.ini[/purple][/blue3]")

console.print(
    "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]\n\n"
)

console.print(
    """[blue3]
                                    ███╗   ██╗██╗ ██████╗███████╗    ██╗
                                    ████╗  ██║██║██╔════╝██╔════╝    ██║
                                    ██╔██╗ ██║██║██║     █████╗      ██║
                                    ██║╚██╗██║██║██║     ██╔══╝      ╚═╝
                                    ██║ ╚████║██║╚██████╗███████╗    ██╗
                                    ╚═╝  ╚═══╝╚═╝ ╚═════╝╚══════╝    ╚═╝

[/blue3]""",
    justify="full",
)

console.print(
    "[blue3]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/blue3]\n\n"
)

console.print("[blue3]> All Checks Have Been Completed.[/blue3]\n")

console.print("[blue3]> LAUNCHING MAIN BOT.[/blue3]\n")


try:
    time.sleep(3)
    os.system("title [Mai] - Bot")
    subprocess.call(["python", "mai.py"])
except Exception as e:
    WaitAndExit(f"BOT COULD NOT BE RUN {e}")
