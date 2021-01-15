import argparse
from .pycritty import subparsers, formatter


set_parser = subparsers.add_parser(
    'set',
    formatter_class=formatter(),
    help="Set a new configuration",
    argument_default=argparse.SUPPRESS,
)

set_parser.add_argument(
    '-t', '--theme',
    dest='change_theme',
    metavar='THEME',
    help='Change theme, choose from ~/.config/alacritty/themes',
)
set_parser.add_argument(
    '-f', '--font',
    dest='change_font',
    metavar='FONT',
    help='Change font family, choose from ~/.config/alacritty/fonts.yaml',
)
set_parser.add_argument(
    '-s', '--size',
    type=float,
    dest='change_font_size',
    metavar='SIZE',
    help='Change font size',
)
set_parser.add_argument(
    '-o', '--opacity',
    type=float,
    dest='change_opacity',
    metavar='OPACITY',
    help='Change background opacity',
)
set_parser.add_argument(
    '-p', '--padding',
    metavar=('X', 'Y'),
    type=int,
    nargs=2,
    dest='change_padding',
    help='Change window padding X Y values',
)
set_parser.add_argument(
    '-O', '--offset',
    metavar=('X', 'Y'),
    type=int,
    nargs=2,
    dest='change_font_offset',
    help='Change offset, X is space between chars and Y is line height',
)
