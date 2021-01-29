# Custom logging for ttys and files

from sys import stdout, stderr
from enum import Enum


class Color(Enum):
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'

    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    NORMAL = '\033[0m'

    def __str__(self):
        return self.value


def color_print(
    *messages,
    default_color=Color.NORMAL,
    sep=' ',
    end='\n',
    file=stdout,
    flush=False,
):
    """Wrapper around print with color options, it applies colors only on ttys

    >>> color_print(Color.BOLD, 'Home =>', Color.BLUE, '/home/example')
    >>> # "Home =>" would be bold and "/home/example" would be blue

    >>> # Don't mix strings with colors like this:
    >>> color_print(f'{Color.BLUE}This is blue')
    >>> # It will not work when the output is not a tty, the result would be:
    >>> '\033[0;34mThis is blue'
    """

    string = []
    print_colors = file.isatty()
    if print_colors:
        string.append(str(default_color))

    for i in range(len(messages) - 1):
        # Print separators only after strings
        is_color = isinstance(messages[i], Color)
        if not is_color or print_colors:
            string.append(str(messages[i]))
        if not is_color:
            string.append(sep)

    # Last message being a color makes no sense
    if not isinstance(messages[-1], Color):
        string.append(str(messages[-1]))
    if print_colors:
        string.append(str(Color.NORMAL))

    print(''.join(string), end=end, flush=flush, file=file)


def warn(*messages, sep=' ', end='\n', file=stderr, flush=False):
    color_print(
        *messages,
        default_color=Color.YELLOW,
        sep=sep,
        end=end,
        file=file,
        flush=flush,
    )


def err(*messages, sep=' ', end='\n', file=stderr, flush=False):
    color_print(
        *messages,
        default_color=Color.RED,
        sep=sep,
        end=end,
        file=file,
        flush=flush,
    )


def ok(*messages, sep=' ', end='\n', file=stdout, flush=False):
    color_print(
        *messages,
        default_color=Color.GREEN,
        sep=sep,
        end=end,
        file=file,
        flush=flush,
    )
