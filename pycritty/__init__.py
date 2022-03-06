"""Automated tools for managing alacritty configurations"""

__version__ = "0.4.0"


class PycrittyError(Exception):
    pass


# Export public API
from pycritty.api.config import Config, set_config  # noqa: F401, E402
from pycritty.api.install import install  # noqa: F401, E402
from pycritty.api.load import load_config  # noqa: F401, E402
from pycritty.api.save import save_config  # noqa: F401, E402
from pycritty.api.rm import remove  # noqa: F401, E402
from pycritty.api.ls import (  # noqa: F401, E402
    list_themes,
    list_fonts,
    list_configs,
    print_list,
)
