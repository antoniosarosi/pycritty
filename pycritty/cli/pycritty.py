from .. import __version__, PycrittyError
from ..commands.pycritty import Pycritty
import click


class XYFloatPair(click.ParamType):
    name = 'X:Y floats'

    def convert(self, value, param, ctx):
        splitted = value.split(':')
        if len(splitted) != 2:
            self.fail('Expected two values in the form X:Y')

        x, y = splitted

        try:
            x, y = float(x), float(y)
            return x, y
        except ValueError:
            self.fail('Expected two floats in the form X:Y')


@click.group(invoke_without_command=True)
@click.option('-t', '--theme', help='Change theme, choose from ~/.config/alacritty/themes')
@click.option('-f', '--font', help='Change font family, from ~/.config/alacritty/fonts.yaml')
@click.option('-p', '--padding', help='Change window padding X Y values', type=XYFloatPair())
@click.option('-o', '--opacity', help='Change window opacity', type=click.FloatRange(0, 1))
@click.option('-s', '--size', 'font_size', help='Change font size', type=float)
@click.option('-O', '--offset', 'font_offset', help='Change offset, X is space between chars and Y is line height', type=XYFloatPair())
@click.help_option()
@click.version_option(__version__, prog_name='Pycritty')
def pycritty_cli(**options):
    """Change your Alacritty config on the fly!"""


@pycritty_cli.resultcallback()
def pycritty_cli_cb(rest, **options):
    opts = {k: v for k, v in options.items() if v is not None}

    if rest is not None and opts:
        raise PycrittyError(
            "Ambiguous command: Can't know if you want to apply settings first or do the command first!")

    # apply my options
    conf = Pycritty()

    conf.set(**opts)
    conf.apply()
