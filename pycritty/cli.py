from typing import Dict, Any
import argparse
from . import __version__


def args() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(
        prog='pycritty',
        description='Change your Alacritty config on the fly!',
        usage='pycritty [OPTIONS]',
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=80),
        argument_default=argparse.SUPPRESS,
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=__version__
    )
    parser.add_argument(
        '-t', '--theme',
        help='Change theme, choose from ~/.config/alacritty/themes'
    )
    parser.add_argument(
        '-f', '--font',
        help='Change font family, choose from ~/.config/alacritty/fonts.yaml'
    )
    parser.add_argument(
        '-s', '--size',
        type=float,
        help='Change font size'
    )
    parser.add_argument(
        '-o', '--opacity',
        type=float,
        help='Change background opacity'
    )
    parser.add_argument(
        '-p', '--padding',
        metavar=('X', 'Y'),
        type=int,
        nargs=2,
        help='Change window padding X Y values'
    )
    parser.add_argument(
        '-O', '--offset',
        metavar=('X', 'Y'),
        type=int,
        nargs=2,
        help='Change offset, X is space between chars and Y is line height'
    )
    parser.add_argument(
        '-l', '--list',
        nargs='?',
        const='all',
        choices=['fonts', 'themes', 'all'],
        help='List all available options from resource, default is "all"'
    )
    parser.add_argument(
        '-P', '--print',
        nargs='*',
        metavar=('config', 'fonts'),
        help='Print the content of config files or themes by specifying their name',
    )

    return vars(parser.parse_args())
