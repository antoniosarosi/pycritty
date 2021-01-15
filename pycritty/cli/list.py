import argparse
from .pycritty import subparsers, formatter


list_parser = subparsers.add_parser(
    'list',
    help='List available resources',
    formatter_class=formatter(),
    argument_default=argparse.SUPPRESS,
)

list_parser.add_argument(
    'list_resource',
    nargs='*',
    default='all',
    choices=['fonts', 'themes', 'saves', 'all'],
    help='List all available options from a resource, default is "all"',
)
