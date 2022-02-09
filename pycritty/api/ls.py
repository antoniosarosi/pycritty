from typing import List, Dict, Any
from pycritty import PycrittyError
from pycritty.resources import fonts_file, themes_dir, saves_dir
from pycritty.resources.resource import Resource
from pycritty.io import log, yaml_io


def list_dir(directory: Resource):
    return [file.stem for file in directory.path.iterdir()]


def list_themes() -> List[str]:
    if not themes_dir.exists():
        raise PycrittyError(f'Failed listing themes, directory {themes_dir.path} not found')

    return list_dir(themes_dir)


def list_configs() -> List[str]:
    if not saves_dir.exists():
        raise PycrittyError(f'Cannot list saves, {saves_dir} not found')

    return list_dir(saves_dir)


def list_fonts() -> List[str]:
    if not fonts_file.exists():
        raise PycrittyError(f'Failed listing fonts, file {fonts_file.path} not found')

    fonts_yaml = yaml_io.read(fonts_file)
    if fonts_yaml is None or 'fonts' not in fonts_yaml:
        fonts = []
    else:
        fonts = fonts_yaml['fonts'].keys()

    return fonts


def print_list(list_all=True, themes=False, fonts=False, configs=False, iterable=False):
    to_be_listed = {
        'themes': themes,
        'fonts': fonts,
        'configs': configs,
    }

    # Ignore list_all if something else has been specified
    if not any(to_be_listed.values()) and list_all:
        for k in to_be_listed:
            to_be_listed[k] = True
    
    options = {
        'themes': ('Themes', log.Color.BLUE, list_themes),
        'fonts': ('Fonts', log.Color.PURPLE, list_fonts),
        'configs': ('Configs', log.Color.CYAN, list_configs),
    }

    for opt in options:
        if not to_be_listed[opt]:
            continue
        header, color, get_list = options[opt]
        if not iterable:
            log.color_print(f'{header}:', default_color=log.Color.BOLD)
        ls = get_list()
        tabs = '    ' if not iterable else ''
        if len(ls) < 1 and not iterable:
            log.color_print(log.Color.ITALIC, log.Color.YELLOW, f'{tabs}Empty directory')
        else:
            for item in ls:
                log.color_print(f'{tabs}{item}', default_color=color)
