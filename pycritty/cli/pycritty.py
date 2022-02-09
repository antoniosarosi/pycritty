import argparse
from pycritty import __version__


def formatter(indent_increment=2, max_help_position=40, width=None):
    return lambda prog: argparse.HelpFormatter(
        prog,
        indent_increment,
        max_help_position,
        width, 
    )


parser = argparse.ArgumentParser(
    prog='pycritty',
    description='Change your Alacritty config on the fly!',
    argument_default=argparse.SUPPRESS,
    formatter_class=formatter(),
)
parser.add_argument(
    '-v', '--version',
    action='version',
    version=__version__,
)

parser.add_argument(
    '-t', '--theme',
    metavar='THEME',
    help='Change theme, choose from ~/.config/alacritty/themes',
)
parser.add_argument(
    '-f', '--font',
    metavar='FONT',
    help='Change font family, choose from ~/.config/alacritty/fonts.yaml',
)
parser.add_argument(
    '-s', '--font-size',
    type=float,
    dest='font_size',
    metavar='SIZE',
    help='Change font size',
)
parser.add_argument(
    '-o', '--opacity',
    type=float,
    metavar='OPACITY',
    help='Change background opacity',
)
parser.add_argument(
    '-p', '--padding',
    metavar=('X', 'Y'),
    type=int,
    nargs=2,
    help='Change window padding X Y values',
)
parser.add_argument(
    '-O', '--offset',
    metavar=('X', 'Y'),
    type=int,
    nargs=2,
    help='Change offset, X is space between chars and Y is line height',
)

subparsers = parser.add_subparsers(
    title='subcommands',
    dest='subcommand',
)
