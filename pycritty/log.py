from sys import stdout, stderr
from enum import Enum


class Color(Enum):
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'

    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    NORMAL = '\033[0m'

    def __str__(self):
        return self.value


def color_print(message: str, color=Color.NORMAL, file=stdout, **params):
    if file.isatty(): 
        message = f'{color}{message}{Color.NORMAL}'
    print(message, file=file, **params)


def warn(message: str):
    color_print(message, Color.YELLOW, stderr)


def err(message: str):
    color_print(message, Color.RED, stderr)


def ok(message: str):
    color_print(message, Color.GREEN)
