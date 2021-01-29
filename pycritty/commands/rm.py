from typing import Dict, Any, List
from .command import Command
from ..resources import saves_dir, themes_dir
from ..resources.resource import Resource, ConfigFile
from ..io import log


class Remove(Command):
    def remove(self, configs: List[str], config_parent: Resource, force=False):
        for conf in configs:
            file = ConfigFile(config_parent.path, conf, ConfigFile.YAML)
            if not file.exists():
                log.warn(f'{conf} ->', log.Color.BOLD, file, log.Color.YELLOW, 'not found')
                continue
            confirmed = force
            if not confirmed:
                log.color_print(f'Removing {conf} ->', log.Color.BLUE, log.Color.BOLD, file)
                confirmed = 'y' in input('Confirm (y/n): ').lower()
            if confirmed:
                file.path.unlink()

    def execute(self, actions: Dict[str, Any]):
        if 'configs' not in actions:
            return
        force = 'force' in actions
        config_parent = themes_dir if 'theme' in actions else saves_dir
        self.remove(actions['configs'], config_parent, force)
