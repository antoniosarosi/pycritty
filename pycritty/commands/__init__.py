from .set import SetConfig
from .list import ListResource
from .save import SaveConfig
from .load import LoadConfig
from .install import Install

subcommands = {
    'set': SetConfig,
    'list': ListResource,
    'save': SaveConfig,
    'load': LoadConfig,
    'install': Install,
}
