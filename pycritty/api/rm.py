from typing import List

from pycritty.io import log
from pycritty.resources import saves_dir, themes_dir
from pycritty.resources.resource import ConfigFile


def remove(configs: List[str], from_themes=False, force=False):
    config_parent = themes_dir if from_themes else saves_dir
    for conf in configs:
        file = ConfigFile(config_parent.path, conf, ConfigFile.FILES)
        if not file.exists():
            log.warn(f'{conf} ->', log.Color.BOLD, file, log.Color.YELLOW, 'not found')
            continue
        confirmed = force
        if not confirmed:
            log.color_print(f'Removing {conf} ->', log.Color.BLUE, log.Color.BOLD, file)
            confirmed = 'y' in input('Confirm (y/n): ').lower()
        if confirmed:
            file.path.unlink()
