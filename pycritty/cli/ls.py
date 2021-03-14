from .pycritty import pycritty_cli
from ..commands.ls import ListResource
import click


@pycritty_cli.command('ls')
@click.option('-t', '--themes', is_flag=True,  help='List themes')
@click.option('-f', '--fonts', is_flag=True,  help='List fonts')
@click.option('-c', '--configs', is_flag=True,  help='List configs')
@click.option('-a', '--all', is_flag=True,  help='List all')
@click.option('-i', '--iterable', is_flag=True, help='List in iterable format (for scripts)')
def ls(**options):
    """List available resources"""
    return ListResource, { k:v for k, v in options.items() if v }
