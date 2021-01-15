import argparse
from .pycritty import subparsers, formatter


save_parser = subparsers.add_parser(
    'save',
    formatter_class=formatter(),
    help="Save the current config to reuse it later",
    argument_default=argparse.SUPPRESS,
)

save_parser.add_argument(
    'save_config',
    metavar='NAME',
    help='Name of the config being saved',
)

save_parser.add_argument(
    '-o', '--override',
    dest='override_config',
    action='store_true',
    help='Override existing config',
)