from typing import Dict, Callable, Any, Optional
import pycritty


class Cli:
    commands: Dict[str, Callable[..., None]]

    def __init__(self):
        self.commands = {}

    def define_command(self, name: str, action: Callable[..., None]):
        self.commands[name] = action

    def define_commands(self, commands: Dict[str, Callable[..., None]]):
        self.commands = commands

    def execute(self, command: Optional[str], args: Dict[str, Any]):
        if command is None:
            command = "pycritty"
        if command not in self.commands:
            raise pycritty.PycrittyError(f"Unkown command {command}")

        executable_command = self.commands[command]
        executable_command(**args)


cli = Cli()

cli.define_commands({
    'pycritty': pycritty.set_config,
    'ls': pycritty.print_list,
    'rm': pycritty.remove,
    'save': pycritty.save_config,
    'load': pycritty.load_config,
    'install': pycritty.install,
})
