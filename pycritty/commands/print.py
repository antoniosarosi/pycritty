from typing import List
import yaml
from .command import Command
from .. import resources
from ..io import log, yio


class Printer(Command):
    def print_yaml(self, resource: resources.ConfigFile):
        if not resource.exists():
            log.warn(f'{resource.path} not found')
            return

        content = yio.read_yaml(resource.path)
        log.color_print(resource.path, default_color=log.Color.BOLD)
        if content is None or len(content) == 0:
            log.warn('File is empty')
        else:
            print(yaml.dump(content))

    def print(self, to_be_printed: List[str]):
        options = {
            'fonts': resources.fonts_file,
            'config': resources.config_file,
        }

        for file in to_be_printed:
            if file not in options:
                self.print_yaml(resources.get_theme(file))
            else:
                self.print_yaml(options[file])
