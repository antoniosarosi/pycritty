from pathlib import Path
from pycritty.resources.resource import ConfigFile,  ConfigDir


pycritty_dir = ConfigDir(Path().home() / '.config' / 'pycritty')
alacritty_dir = ConfigDir(Path().home() / '.config' / 'alacritty')
config_file = ConfigFile(alacritty_dir.path, 'alacritty', ConfigFile.YAML)
fonts_file = ConfigFile(pycritty_dir.path, 'fonts', ConfigFile.YAML)
themes_dir = ConfigDir(pycritty_dir.path / 'themes')
saves_dir = ConfigDir(pycritty_dir.path / 'saves')


def get_theme(theme: str) -> ConfigFile:
    return ConfigFile(themes_dir.get_or_create(), theme, ConfigFile.YAML)
