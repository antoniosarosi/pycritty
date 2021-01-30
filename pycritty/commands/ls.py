from typing import List, Dict, Any
from .command import Command
from .. import PycrittyError
from ..resources import fonts_file, themes_dir, saves_dir
from ..resources.resource import Resource
from ..io import log
from ..io.yio import read_yaml


class ListResource(Command):
    def __init__(self):
        self.options = {
            'themes': ('Themes', log.Color.BLUE, self.list_themes),
            'fonts': ('Fonts', log.Color.PURPLE, self.list_fonts),
            'configs': ('Configs', log.Color.CYAN, self.list_configs),
        }

    def _list_dir(self, directory: Resource):
        return [file.stem for file in directory.path.iterdir()]

    def list_themes(self) -> List[str]:
        if not themes_dir.exists():
            raise PycrittyError(
                f'Failed listing themes, directory {themes_dir.path} not found'
            )

        return self._list_dir(themes_dir)

    def list_configs(self) -> List[str]:
        if not saves_dir.exists():
            raise PycrittyError(f'Cannot list saves, {saves_dir} not found')

        return self._list_dir(saves_dir)

    def list_fonts(self) -> List[str]:
        if not fonts_file.exists():
            raise PycrittyError(
                f'Failed listing fonts, file {fonts_file.path} not found'
            )

        fonts_yaml = read_yaml(fonts_file)
        if fonts_yaml is None or 'fonts' not in fonts_yaml:
            fonts = []
        else:
            fonts = fonts_yaml['fonts'].keys()

        return fonts

    def print_list(self, option: str, iterable=True):
        header, color, get_list = self.options[option]
        if not iterable:
            log.color_print(f'{header}:', default_color=log.Color.BOLD)
        ls = get_list()
        tabs = '    ' if not iterable else ''
        if len(ls) < 1 and not iterable:
            log.color_print(log.Color.ITALIC, log.Color.YELLOW, f'{tabs}Empty directory')
        else:
            for item in ls:
                log.color_print(f'{tabs}{item}', default_color=color)
            
    def execute(self, args: Dict[str, Any]):
        iterable = False
        if 'iterable' in args:
            iterable = True
            args.pop('iterable')
        if len(args) < 1:
            args['all'] = True
        if 'all' in args:
            for opt in self.options:
                args[opt] = True
            args.pop('all')
        for opt in args:
            self.print_list(opt, iterable)
