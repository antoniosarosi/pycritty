# Pycritty
# Antonio Sarosi
# December 9, 2020

from . import PycrittyError
from .io import log
from .commands import subcommands, SetConfig
from .cli import parser


def main():
    args = vars(parser.parse_args())
    if args['subcommand'] is None:
        command_receiver = SetConfig
    else:
        command_receiver = subcommands[args['subcommand']]
    args.pop('subcommand')
    if command_receiver.requires_args and len(args) < 1:
        parser.print_help()
        exit(0)
    try:
        command_receiver().execute(args)
    except PycrittyError as e:
        log.err(e)
        exit(1)


if __name__ == '__main__':
    main()
