from sys import stdout, stderr
from enum import Enum


class Color(Enum):
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    RESET = '\033[0m'

    def __str__(self):
        return self.value


def color_print(color: Color, message, output=stdout):
    print(f'{color}{message}{Color.RESET}', file=output)


def warn(message: str):
    color_print(Color.YELLOW, message, stderr)


def err(message: str):
    color_print(Color.RED, message, stderr)


def msg(message: str):
    color_print(Color.GREEN, message)
