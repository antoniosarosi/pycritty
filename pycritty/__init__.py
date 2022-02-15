"""Automated tools for managing alacritty configurations"""

__version__ = "0.4.0"


class PycrittyError(Exception):
    pass


# Export public API
from pycritty.api.config import Config, set_config
from pycritty.api.install import install
from pycritty.api.load import load_config
from pycritty.api.save import save_config
from pycritty.api.rm import remove
from pycritty.api.ls import list_themes, list_fonts, list_configs, print_list
