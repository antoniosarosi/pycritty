from .set import SetConfig
from .print import Printer
from .list import ListResource
from .save import SaveConfig
from .load import LoadConfig
from .install import Install

subcommands = {
    'set': SetConfig,
    'print': Printer,
    'list': ListResource,
    'save': SaveConfig,
    'load': LoadConfig,
    'install': Install,
}
