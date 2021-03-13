# Pycritty
# Antonio Sarosi
# December 2020

from .cli import pycritty_cli
from .io import log
from . import PycrittyError

def main():
    try:
        pycritty_cli()
    except (PycrittyError, KeyboardInterrupt) as e:
        if isinstance(e, KeyboardInterrupt):
            e = 'Interrupted, changes might not have been applied'
        log.err(e)

if __name__ == '__main__':
    pycritty_cli()
