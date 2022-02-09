import argparse
from pycritty.cli import subparsers, formatter


install_parser = subparsers.add_parser(
    'install',
    formatter_class=formatter(),
    help="Install a config file or theme from a url",
    argument_default=argparse.SUPPRESS,
)

install_parser.add_argument(
    'url',
    help='URL where the config is located',
)

install_parser.add_argument(
    '-n', '--name',
    metavar='NAME',
    dest='config_name',
    default='',
    help='Name of the config/theme once installed',
)

install_parser.add_argument(
    '-o', '--override',
    action='store_true',
    help='Override existing config',
)

group = install_parser.add_mutually_exclusive_group()

group.add_argument(
    '-t', '--theme',
    dest='as_theme',
    action='store_true',
    help='Install as theme',
)

group.add_argument(
    '-c', '--config',
    action='store_true',
    help='Install as a config file in your saves directory (default)',
)
