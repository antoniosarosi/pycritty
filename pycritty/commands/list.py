from typing import List
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
            'saves': ('Saves', log.Color.CYAN, self.list_saves),
        }

    def _list_dir(self, directory: Resource):
        return [file.stem for file in directory.path.iterdir()]

    def list_themes(self) -> List[str]:
        if not themes_dir.exists():
            raise PycrittyError(
                f'Failed listing themes, directory {themes_dir.path} not found'
            )

        return self._list_dir(themes_dir)

    def list_saves(self) -> List[str]:
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

    def print_list(self, option: str):
        header, color, get_list = self.options[option]
        log.color_print(f'{header}:', default_color=log.Color.BOLD)
        for item in get_list():
            log.color_print(f'    {item}', default_color=color)

    def list_resource(self, to_be_listed: List[str]):
        if 'all' in to_be_listed:
            for opt in self.options:
                self.print_list(opt)
            return

        incorrenct_options = []
        for opt in to_be_listed:
            if opt not in self.options:
                incorrenct_options.append(opt)
            else:
                self.print_list(opt)

        if len(incorrenct_options) > 0:
            raise PycrittyError(
                f'Failed listing "{",".join(incorrenct_options)}" (unknown options)'
            )