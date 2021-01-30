from typing import Dict, Any
from abc import ABCMeta, abstractmethod


class Command(metaclass=ABCMeta):
    """Objects representing a CLI command"""

    @abstractmethod
    def execute(self, actions: Dict[str, Any]):
        """Actions are key value pairs parsed from sys.argv with argparse.
        For example, the command that sets configs might receive this:
        >>> {'set_theme': 'onedark', 'set_font': 'UbuntuMono'}
        The command that installs configs might receive something like this:
        >>> {'url': 'https://example.io./conf.yml', 'override': True, 'name': 'Foo'}
        These key value pairs have to be interpreted as arguments or callable
        functions, depending on the command.
        """
        pass
