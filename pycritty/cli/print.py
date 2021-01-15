import argparse
from .pycritty import subparsers, formatter


print_parser = subparsers.add_parser(
    'print',
    help='Print the contents of a config file',
    formatter_class=formatter(max_help_position=10),
    argument_default=argparse.SUPPRESS,
)

print_parser.add_argument(
    'print',
    nargs='*',
    default=['config'],
    help='Choose from "config", "fonts", or a theme name like "onedark"',
)
