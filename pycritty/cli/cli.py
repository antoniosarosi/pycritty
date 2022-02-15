from typing import Dict, Callable, Any
import pycritty


class Cli:
    def __init__(self):
        self.commands: Dict[str, Callable[[Any, ...], None]] = {}

    def define_command(self, name: str, action: Callable[[Any, ...], None]):
        self.commands[name] = action
        
    def define_commands(self, commands: Dict[str, Callable[[Any, ...], None]]):
        self.commands = commands

    def execute(self, command: str, args: Dict[str, Any]):
        if command is None:
            command = 'pycritty'
        if command not in self.commands:
            raise pycritty.PycrittyError(f'Unkown command {command}')

        command = self.commands[command]
        command(**args)


cli = Cli()

cli.define_commands({
    'pycritty': pycritty.set_config,
    'ls': pycritty.print_list,
    'rm': pycritty.remove,
    'save': pycritty.save_config,
    'load': pycritty.load_config,
    'install': pycritty.install,
})
