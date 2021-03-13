# Pycritty
# Antonio Sarosi
# December 2020

# from . import PycrittyError
# from .io import log
# from .commands import subcommands, Pycritty
# from .cli import parser

from .cli import pycritty_cli

# def main():
#     args = vars(parser.parse_args())
#     if args['subcommand'] is None:
#         command_receiver = Pycritty
#     else:
#         command_receiver = subcommands[args['subcommand']]
#     args.pop('subcommand')
#     try:
#         command_receiver().execute(args)
#     except (PycrittyError, KeyboardInterrupt) as e:
#         if isinstance(e, KeyboardInterrupt):
#             e = 'Interrupted, changes might not have been applied'
#         log.err(e)
#         exit(1)

def main():
    pycritty_cli()

if __name__ == '__main__':
    pycritty_cli()
