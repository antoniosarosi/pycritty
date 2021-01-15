# YAML IO

from typing import Dict, Any, Union
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import URLError
from pathlib import Path
import yaml
from ..resources.resource import Resource
from .. import PycrittyError


class YamlIOError(PycrittyError):
    pass


class YamlParseError(PycrittyError):
    pass


def read_yaml(url: Union[str, Path, Resource]) -> Dict[str, Any]:
    """Read YAML from a URL or from the local file system

    >>> y1 = read_yaml('https://example.io/config.yaml')
    {'example': 'test'}
    >>> y2 = read_yaml(Path().home() / 'example.yaml')
    {'another_example': 123}
    """

    has_protocol = False
    if isinstance(url, str):
        has_protocol = urlparse(url).scheme != ''
    if isinstance(url, Resource):
        url = url.path
    if not has_protocol or isinstance(url, Path) or isinstance(url, Resource):
        open_function = open
    else:
        open_function = urlopen

    try:
        with open_function(url) as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    except (IOError, URLError) as e:
        raise YamlIOError(f'Error trying to access "{url}":\n{e}')
    except yaml.YAMLError as e:
        raise YamlParseError((
            'YAML error at "{0}", '
            'at line {1.problem_mark.line}, '
            'column {1.problem_mark.column}:\n'
            '{1.problem} {1.context}'
        ).format(url, e))


def write_yaml(y: Dict[str, Any], file: Union[Path, Resource]):
    """Write YAML to a file in the local system

    >>> write_yaml({'example': 123}, Path().home() / 'exmaple.yaml')
    """

    if isinstance(file, Resource):
        file = file.path
    try:
        with open(file, 'w') as f:
            yaml.dump(y, f)
    except IOError as e:
        raise YamlIOError(f'Failed writing to {file}:\n{e}')
