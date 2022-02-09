import argparse
from pycritty.cli import subparsers, formatter


save_parser = subparsers.add_parser(
    'save',
    formatter_class=formatter(),
    help="Save the current config to reuse it later",
    argument_default=argparse.SUPPRESS,
)

save_parser.add_argument(
    'name',
    metavar='NAME',
    help='Name of the config being saved',
)

save_parser.add_argument(
    '-o', '--override',
    action='store_true',
    help='Override existing config',
)
