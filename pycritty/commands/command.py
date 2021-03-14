from typing import Dict, Callable, Any
from .. import PycrittyError


class Pycritty:
    def __init__(self):
        self.commands: Dict[str, Callable[[Any, ...], None]] = {}

    def command(self, name: str) -> Callable[Callable[[Any, ...], None], None]:
        def register(callback):
            self.commands[name] = callback
            return callback

        return register

    def execute(self, command: str, args: Dict[str, Any]):
        if command is None:
            command = 'pycritty'
        if command not in self.commands:
            raise PycrittyError(f'Unkown command {command}')

        command = self.commands[command]
        command(**args)


pycritty = Pycritty()
