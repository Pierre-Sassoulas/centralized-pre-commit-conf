from typing import Union

from colorama import Fore, init

init()


def echo(color: Fore, message: Union[Warning, str]) -> None:
    print(f"{color}{message}{Fore.RESET}")


def info(message: str) -> None:
    echo(Fore.BLUE, message)


def warn(message: Union[Warning, str]) -> None:
    echo(Fore.YELLOW, message)


def error(message: str) -> None:
    echo(Fore.RED, message)


def success(message: str) -> None:
    echo(Fore.GREEN, message)
