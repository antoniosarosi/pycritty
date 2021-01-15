from .command import Command
from .. import PycrittyError
from ..io import log, yio
from ..resources import saves_dir, config_file, ConfigFile


class LoadConfig(Command):
    def load_config(self, config_name: str):
        file_to_load = ConfigFile(saves_dir.get_or_create(), config_name, ConfigFile.YAML)
        if not file_to_load.exists():
            raise PycrittyError(f'Config "{config_name}" not found')

        conf = yio.read_yaml(file_to_load)
        if conf is None or len(conf) < 1:
            log.warn(f'"{file_to_load}" has no content')
        else:
            yio.write_yaml(conf, config_file)

        log.ok(f'Config "{config_name}" applied')
