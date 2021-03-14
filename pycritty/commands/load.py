from typing import Dict, Any
from .. import PycrittyError
from ..io import log, yio
from ..resources import saves_dir, config_file, ConfigFile
from .command import pycritty


@pycritty.command('load')
def load_config(name: str):
    file_to_load = ConfigFile(saves_dir.get_or_create(), name, ConfigFile.YAML)
    if not file_to_load.exists():
        raise PycrittyError(f'Config "{name}" not found')

    conf = yio.read_yaml(file_to_load)
    if conf is None or len(conf) < 1:
        log.warn(f'"{file_to_load}" has no content')
    else:
        yio.write_yaml(conf, config_file)

    log.ok(f'Config "{name}" applied')
