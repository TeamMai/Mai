"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

from .console import console


class ASCII:
    def ERROR(self) -> None:
        console.print(
            """[red]

                        ███████╗██████╗ ██████╗  ██████╗ ██████╗         ██╗
                        ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗    ██╗██╔╝
                        █████╗  ██████╔╝██████╔╝██║   ██║██████╔╝    ╚═╝██║
                        ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██╗    ██╗██║
                        ███████╗██║  ██║██║  ██║╚██████╔╝██║  ██║    ╚═╝╚██╗
                        ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝        ╚═╝

        [/red]""",
            justify="full",
        )

    def LINE(self) -> None:
        console.print(
            "[red]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/red]"
        )
