#!/usr/bin/env python3

# Pycritty
# Antonio Sarosi
# December 9, 2020

from typing import Dict, Any
import argparse
from alacritty import Alacritty, ConfigError
import log


VERSION = 'v0.1.0'


def args() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(
        prog='pycritty',
        description='Change your Alacritty config on the fly!',
        usage='pycritty [OPTIONS]',
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=80),
        argument_default=argparse.SUPPRESS,
    )
    parser.add_argument('-v', '--version', action='version', version=VERSION)
    parser.add_argument('-t', '--theme', metavar='"Theme name"')
    parser.add_argument('-f', '--font', metavar='"Font alias"')
    parser.add_argument('-s', '--size', type=float)
    parser.add_argument('-o', '--opacity', type=float)
    parser.add_argument('-p', '--padding', type=int, nargs=2, metavar=('x', 'y'))
    parser.add_argument(
        '-l', '--list', nargs='?', const='all', choices=['fonts', 'themes', 'all']
    )

    return vars(parser.parse_args())


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
