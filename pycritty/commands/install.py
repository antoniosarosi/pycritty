from typing import Dict, Any, Union
from urllib.parse import urlparse
from pathlib import Path
from .command import Command
from .save import SaveConfig
from ..resources import saves_dir, themes_dir
from ..resources.resource import Resource


class Install(Command):
    def __init__(self):
        self.save = SaveConfig()

    def install(
        self,
        config_name: str,
        url: Union[str, Path, Resource],
        dest_parent=saves_dir,
        override=False
    ):
        """Download config from a URL

        >>> from pycritty.resources import themes_dir
        >>> installer = Install()
        >>> installer.install(
        ...     config_name='example',
        ...     url='https://example.com/config.yaml',
        ...     dest_parent=themes_dir,
        ...     override=True,
        ... )
        """

        self.save.save_config(config_name, url, dest_parent, override)

    def execute(self, actions: Dict[str, Any]):
        if 'url' not in actions:
            return

        url = actions['url']
        name = actions['name']
        if name is None or len(name) == 0:
            name = Path(urlparse(url).path).stem

        override = 'override_config' in actions
        dest_parent = saves_dir
        if 'theme' in actions:
            dest_parent = themes_dir

        self.install(name, url, dest_parent, override)
