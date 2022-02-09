# YAML IO

from typing import Dict, Any, Union
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import URLError
from pathlib import Path
import yaml
from pycritty.resources.resource import Resource
from pycritty import PycrittyError


class YamlIOError(PycrittyError):
    pass


class YamlParseError(PycrittyError):
    pass


def read(url: Union[str, Path, Resource]) -> Dict[str, Any]:
    """Read YAML from a URL or from the local file system

    >>> y1 = read('https://example.io/config.yaml')
    {'example': 'test'}
    >>> y2 = read(Path().home() / 'example.yaml')
    {'another_example': 123}
    """

    has_protocol = False
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
        raise YamlIOError(f'Error trying to access "{url}":\n{e}')
    except (UnicodeDecodeError, yaml.reader.ReaderError) as e:
        raise YamlParseError(f'Failed decoding "{url}":\n{e}')
    except yaml.YAMLError as e:
        raise YamlParseError((
            f'YAML error at "{url}", '
            f'at line {e.problem_mark.line}, '
            f'column {e.problem_mark.column}:\n'
            f'{e.problem} {e.context or ""}'
        ))


def write(y: Dict[str, Any], file: Union[Path, Resource]):
    """Write YAML to a file in the local system

    >>> write({'example': 123}, Path().home() / 'exmaple.yaml')
    """

    if isinstance(file, Resource):
        file = file.path
    try:
        with open(file, 'w') as f:
            yaml.dump(y, f)
    except IOError as e:
        raise YamlIOError(f'Failed writing to {file}:\n{e}')
