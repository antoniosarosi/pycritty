from .pycritty import pycritty_cli
from ..commands.install import Install
import click
from urllib.parse import urlparse


class ValidURL(click.ParamType):
    name = "URL"

    def convert(self, value, param, ctx):
        try:
            urlparse(value)
            return value
        except:
            self.fail(f"Not a valid URL: {value!r}")


@pycritty_cli.command('install')
@click.argument('url', type=ValidURL)
@click.option('-n', '--name', help='Name to save the configuration as. Derived from URL if not present')
@click.option('-o', '--override', help='Override existing config')
@click.option('-t', '--theme', 'is_theme', is_flag=True, help='Install as theme instead of config file')
def install(url, name='', override=False, is_theme=False):
    """Install a config file from the Internet right into your saves folder"""
    opts = dict(url=url, name=name, override=override)
    if is_theme:
        opts['theme'] = True

    return Install, opts
