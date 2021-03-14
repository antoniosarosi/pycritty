from .pycritty import pycritty_cli
from ..commands.rm import Remove
import click


@pycritty_cli.command('rm')
@click.argument('configs', nargs=-1)
@click.option('-t', '--theme', 'is_theme', is_flag=True, help='Remove theme file instead of saved config file')
@click.option('-f', '--force', is_flag=True, help="Don't prompt for confirmation")
def rm(configs, is_theme=False, force=False):
    """Remove config files (themes or saves)"""

    actions = {'configs': configs, 'force': force}

    if is_theme:
        actions['theme'] = True

    return Remove, actions
