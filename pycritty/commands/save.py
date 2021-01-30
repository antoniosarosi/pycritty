from typing import Dict, Any, Union
from pathlib import Path
from .. import PycrittyError
from .command import Command
from ..io import log, yio
from ..resources import config_file, saves_dir
from ..resources.resource import ConfigFile


class SaveConfig(Command):
    def save_config(
        self,
        config_name: str,
        read_from: Union[str, Path, ConfigFile] = config_file,
        dest_parent=saves_dir,
        override=False
    ):
        dest_file = ConfigFile(dest_parent.get_or_create(), config_name, ConfigFile.YAML)
        if dest_file.exists() and not override:
            raise PycrittyError(
                f'Config "{config_name}" already exists, use -o to override'
            )

        conf = yio.read_yaml(read_from)
        if conf is None or len(conf) < 1:
            log.warn(f'"{read_from}" has no content')
        else:
            dest_file.create()
            yio.write_yaml(conf, dest_file)
            log.ok('Config saved =>', log.Color.BLUE, dest_file)

    def execute(self, actions: Dict[str, Any]):
        config_name = actions['name']
        override = 'override' in actions
        self.save_config(config_name, override=override)
