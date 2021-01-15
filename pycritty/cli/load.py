import argparse
from .pycritty import subparsers, formatter


load_parser = subparsers.add_parser(
    'load',
    formatter_class=formatter(),
    help="Load a saved config",
    argument_default=argparse.SUPPRESS,
)

load_parser.add_argument(
    'load_config',
    metavar='NAME',
    help='Name of the config you want to load',
)
