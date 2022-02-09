import argparse
from pycritty.cli import subparsers, formatter


load_parser = subparsers.add_parser(
    'load',
    formatter_class=formatter(),
    help="Load a saved config",
    argument_default=argparse.SUPPRESS,
)

load_parser.add_argument(
    'name',
    metavar='NAME',
    help='Name of the config you want to load',
)
