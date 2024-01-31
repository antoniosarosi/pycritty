from io import BufferedRandom
from pathlib import Path
from typing import Dict, Any, Union, Callable
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen

import toml

from pycritty.io.error import FileIOError, FileParseError
from pycritty.resources.resource import Resource


def write(y: Dict[str, Any], file: Union[Path, Resource]):
    if isinstance(file, Resource):
        file = file.path
    try:
        with open(file, 'w') as f:
            toml.dump(y, f)
    except IOError as e:
        raise FileIOError(f'Error trying to write "{file}":\n{e}')


def read(url: Union[str, Path, Resource]) -> Dict[str, Any]:
    has_protocol = False
    open_function: Callable[..., BufferedRandom]

    if isinstance(url, str):
        has_protocol = urlparse(url).scheme != ''
    if isinstance(url, Resource):
        url = url.path
    if not has_protocol or isinstance(url, Path):
        open_function = open
    else:
        open_function = urlopen

    try:
        with open_function(url) as f:
            return toml.load(f)
    except (IOError, URLError) as e:
        raise FileIOError(f'Error trying to access "{url}":\n{e}')
    except (UnicodeDecodeError, toml.decoder.TomlDecodeError) as e:
        raise FileParseError(f'Failed decoding "{url}":\n{e}')
