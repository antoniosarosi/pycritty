# YAML IO

from io import BufferedRandom
from typing import Callable, Dict, Any, Union
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import URLError
from pathlib import Path
from pycritty.resources.resource import Resource
from pycritty.io.error import FileIOError, FileParseError
import yaml

def read(url: Union[str, Path, Resource]) -> Dict[str, Any]:
    """Read YAML from a URL or from the local file system

    >>> y1 = read('https://example.io/config.yaml')
    {'example': 'test'}
    >>> y2 = read(Path().home() / 'example.yaml')
    {'another_example': 123}
    """

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
            return yaml.load(f, Loader=yaml.FullLoader)
    except (IOError, URLError) as e:
        raise FileIOError(f'Error trying to access "{url}":\n{e}')
    except (UnicodeDecodeError, yaml.reader.ReaderError) as e:
        raise FileParseError(f'Failed decoding "{url}":\n{e}')
    except yaml.MarkedYAMLError as e:
        raise FileParseError(
            f"YAML error at {url}, "
            f"{e.problem_mark and 'at line ' + str(e.problem_mark.line)}, "
            f"{e.problem_mark and 'column ' + str(e.problem_mark.column)}:\n"
            f"{e.problem} {e.context or ''}"
        )
