from .pycritty import SetConfig
from .ls import ListResource
from .save import SaveConfig
from .load import LoadConfig
from .install import Install
from .rm import Remove

subcommands = {
    'ls': ListResource,
    'save': SaveConfig,
    'load': LoadConfig,
    'install': Install,
    'rm': Remove,
}
