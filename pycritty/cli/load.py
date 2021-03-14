from .pycritty import pycritty_cli
from ..commands.load import LoadConfig
import click


@pycritty_cli.command('load')
@click.argument('config')
def load(config):
    """Load a saved config"""

    return LoadConfig, { 'load_config' : config }

