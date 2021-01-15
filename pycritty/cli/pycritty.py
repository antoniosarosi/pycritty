import argparse
from .. import __version__


def formatter(indent_increment=2, max_help_position=40, width=None):
    return lambda prog: argparse.HelpFormatter(
        prog,
        indent_increment,
        max_help_position,
        width, 
    )


parser = argparse.ArgumentParser(
    prog='pycritty',
    description='Change your Alacritty config on the fly!',
    argument_default=argparse.SUPPRESS,
    formatter_class=formatter(max_help_position=17),
)

parser.add_argument(
    '-v', '--version',
    action='version',
    version=__version__,
)

subparsers = parser.add_subparsers(title='Subcommands', dest='subcommand',)
