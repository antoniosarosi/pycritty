# Pycritty
# Antonio Sarosi
# December 9, 2020

from .alacritty import Alacritty, ConfigError
from .cli import args
from . import log


def main():
    try:
        alacritty = Alacritty()
        alacritty.apply(**args())
        alacritty.save()
    except ConfigError as e:
        log.err(e)
        exit(1)


if __name__ == '__main__':
    main()
