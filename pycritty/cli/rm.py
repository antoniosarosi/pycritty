import argparse
from pycritty.cli import subparsers, formatter


remove_parser = subparsers.add_parser(
    'rm',
    help='Remove config files (themes or saves)',
    formatter_class=formatter(),
    argument_default=argparse.SUPPRESS,
)

remove_parser.add_argument(
    'configs',
    metavar='name',
    nargs='+',
    help='Themes or saved configs to be removed',
)

group = remove_parser.add_mutually_exclusive_group()

group.add_argument(
    '-c', '--config',
    action='store_true',
    help='Remove saved config (default)',
)

group.add_argument(
    '-t', '--theme',
    dest='from_themes',
    action='store_true',
    help='Remove theme',
)

remove_parser.add_argument(
    '-f', '--force',
    action='store_true',
    help="Don't prompt for confirmation",
)
