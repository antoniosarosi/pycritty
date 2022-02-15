from typing import Dict, Any, Union
from urllib.parse import urlparse
from pathlib import Path
from pycritty.resources import saves_dir, themes_dir
from pycritty.resources.resource import Resource
from pycritty.api.save import save_config


def install(
    config_name: str = None,
    url: Union[str, Path, Resource] = None,
    as_theme=False,
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

    if config_name is None or len(config_name) == 0:
        config_name = Path(urlparse(url).path).stem
    dest_parent = themes_dir if as_theme else saves_dir
    save_config(config_name, url, dest_parent, override)
