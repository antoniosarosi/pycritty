#!/usr/bin/env python

# Pycritty
# Antonio Sarosi
# December 9, 2020

from sys import stderr
from alacritty import Alacritty, ConfigError
import argparse


def main():    
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('-t', '--theme', type=str, help='Color scheme')
    parser.add_argument('-f', '--font', type=str, help='Terminal font')
    parser.add_argument('-s', '--size', type=float, help='Font size')
    parser.add_argument('-o', '--opacity', type=float, help='Transparency')
    parser.add_argument('-p', '--padding', type=int, nargs=2, help='Padding')

    config = vars(parser.parse_args())

    try:
        alacritty = Alacritty()
        alacritty.apply(**config)
        alacritty.save()
    except ConfigError as e:
        print(e, file=stderr)
        exit(1)


if __name__ == "__main__":
    main()
