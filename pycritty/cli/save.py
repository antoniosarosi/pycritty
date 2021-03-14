from .pycritty import pycritty_cli
from ..commands.save import SaveConfig
import click


@pycritty_cli.command('save')
@click.argument('name')
@click.option('-o', '--override', is_flag=True, help='Override existing config')
def save(name, override=False):
    actions = {'name': name, 'override': override}

    return SaveConfig, actions
