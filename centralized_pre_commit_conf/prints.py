from colorama import Fore, init

init()


def info(message):
    print(f"{Fore.BLUE}{message}{Fore.RESET}")


def warn(message):
    print(f"{Fore.YELLOW}{message}{Fore.RESET}")


def error(message):
    print(f"{Fore.RED}{message}{Fore.RESET}")


def success(message):
    print(f"{Fore.GREEN}{message}{Fore.RESET}")
