# Pycritty
# Antonio Sarosi
# December 2020

from pycritty import PycrittyError
from pycritty.io import log
from pycritty.cli import parser, cli


def fail(err):
    log.err(err)
    exit(1)


def main():
    args = vars(parser.parse_args())
    subcommand = args.pop('subcommand')
    if len(args) < 1:
        parser.print_help()
        exit(0)
    try:
        cli.execute(subcommand, args)
    except PycrittyError as e:
        fail(e)
    except KeyboardInterrupt:
        fail('Interrupted, changes might not have been applied')


if __name__ == '__main__':
    main()
