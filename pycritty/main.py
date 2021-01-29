# Pycritty
# Antonio Sarosi
# December 9, 2020

from . import PycrittyError
from .io import log
from .commands import subcommands, SetConfig
from .cli import parser


def error(msg: str):
    log.err(msg)
    exit(1)


def main():
    args = vars(parser.parse_args())
    if args['subcommand'] is None:
        command_receiver = SetConfig
    else:
        command_receiver = subcommands[args['subcommand']]
    args.pop('subcommand')
    if len(args) == 0:
        parser.print_help()
        exit(0)
    if command_receiver.requires_args and len(args) < 1:
        error('Missing arguments, use -h for help')
    try:
        command_receiver().execute(args)
    except PycrittyError as e:
        error(e)


if __name__ == '__main__':
    main()
