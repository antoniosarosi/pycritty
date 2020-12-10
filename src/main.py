#!/usr/bin/env python

# Antonio Sarosi
# https://youtube.com/c/antoniosarosi
# https://github.com/antoniosarosi/dotfiles

from sys import stderr
from alacritty import Alacritty, ConfigError
from argparse import ArgumentParser


def main():    
    parser = ArgumentParser()
    parser.add_argument('-t', '--theme', type=str, help='Color scheme')
    parser.add_argument('-f', '--font', type=str, help='Terminal font')
    parser.add_argument('-s', '--size', type=float, help='Font size')
    parser.add_argument('-o', '--opacity', type=float, help='Transparency')
    parser.add_argument('-p', '--padding', type=int, nargs=2, help='Padding')

    args = parser.parse_args()
    
    try:
        alacritty = Alacritty()
        alacritty.change_theme(args.theme)
        alacritty.change_font(args.font, args.size)
        alacritty.change_opacity(args.opacity)
        if args.padding:
            alacritty.change_padding(args.padding[0], args.padding[1])
        alacritty.apply()
    except ConfigError as e:
        print(e, file=stderr)
        exit(1)


if __name__ == "__main__":
    main()
