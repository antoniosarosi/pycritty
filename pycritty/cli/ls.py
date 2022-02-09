import argparse
from pycritty.cli import subparsers, formatter


list_parser = subparsers.add_parser(
    'ls',
    help='List available resources',
    formatter_class=formatter(),
    argument_default=False,
)

list_parser.add_argument(
    '-t', '--themes',
    action='store_true',
    help='List themes',
)

list_parser.add_argument(
    '-f', '--fonts',
    action='store_true',
    help='List fonts',
)

list_parser.add_argument(
    '-c', '--configs',
    action='store_true',
    help='List saved configs',
)

list_parser.add_argument(
    '-a', '--all',
    dest='list_all',
    action='store_true',
    default=True,
    help='List all (default)',
)

list_parser.add_argument(
    '-i', '--iterable',
    action='store_true',
    help='Output list in iterable format (for scripts)',
)
