import sys

from colorama import Fore, init

init()


def echo(color: Fore, message: Warning | str) -> None:
    """Also permits to print emojis on Windows.

    To support non-UTF-8 environments like Windows, we need
    to explicitly encode the message instead of using plain print()
    """
    sys.stdout.buffer.write(f"{color}{message}{Fore.RESET}\n".encode())


def info(message: str) -> None:
    echo(Fore.BLUE, message)


def warn(message: Warning | str) -> None:
    echo(Fore.YELLOW, message)


def error(message: str) -> None:
    echo(Fore.RED, message)


def success(message: str) -> None:
    echo(Fore.GREEN, message)
