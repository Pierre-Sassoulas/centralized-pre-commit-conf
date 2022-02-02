from typing import Union

from colorama import Fore, init

init()


def info(message: str) -> None:
    print(f"{Fore.BLUE}{message}{Fore.RESET}")


def warn(message: Union[Warning, str]) -> None:
    print(f"{Fore.YELLOW}{message}{Fore.RESET}")


def error(message: str) -> None:
    print(f"{Fore.RED}{message}{Fore.RESET}")


def success(message: str) -> None:
    print(f"{Fore.GREEN}{message}{Fore.RESET}")
