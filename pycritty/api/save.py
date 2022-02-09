from typing import Dict, Any, Union
from pathlib import Path
from pycritty import PycrittyError
from pycritty.io import log, yaml_io
from pycritty.resources import config_file, saves_dir, themes_dir
from pycritty.resources.resource import ConfigFile


def save_config(
    name: str,
    read_from: Union[str, Path, ConfigFile] = config_file,
    dest_parent=saves_dir,
    override=False
):
    dest_file = ConfigFile(dest_parent.get_or_create(), name, ConfigFile.YAML)
    word_to_use = "Theme" if dest_parent == themes_dir else "Config"
    if dest_file.exists() and not override:
        raise PycrittyError(f'{word_to_use} "{name}" already exists, use -o to override')

    conf = yaml_io.read(read_from)
    if conf is None or len(conf) < 1:
        log.warn(f'"{read_from}" has no content')
    else:
        dest_file.create()
        yaml_io.write(conf, dest_file)
        log.ok(f'{word_to_use} saved =>', log.Color.BLUE, dest_file)
