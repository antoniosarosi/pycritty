# Pycritty
# Antonio Sarosi
# December 9, 2020

from . import PycrittyError
from .io import log
from .commands import subcommands
from .cli import parser


def main():
    args = vars(parser.parse_args())
    if args['subcommand'] is None:
        parser.print_help()
        exit(0)

    subcommand = subcommands[args['subcommand']]
    args.pop('subcommand')
    if subcommand.requires_args and len(args) < 1:
        log.warn('Missing arguments, use -h for help')
        exit(1)

    try:
        subcommand().execute(args)
    except PycrittyError as e:
        log.err(e)
        exit(1)


if __name__ == '__main__':
    main()
