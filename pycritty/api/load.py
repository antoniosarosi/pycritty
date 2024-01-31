from pycritty import PycrittyError
from pycritty.io import log, toml_io
from pycritty.resources import saves_dir, config_file, ConfigFile


def load_config(name: str):
    file_to_load = ConfigFile(saves_dir.get_or_create(), name, ConfigFile.FILES)
    if not file_to_load.exists():
        raise PycrittyError(f'Config "{name}" not found')

    conf = toml_io.read(file_to_load)
    if conf is None or len(conf) < 1:
        log.warn(f'"{file_to_load}" has no content')
    else:
        toml_io.write(conf, config_file)

    log.ok(f'Config "{name}" applied')
