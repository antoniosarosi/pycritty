# Alacritty config options
# Antonio Sarosi
# December 10, 2020

from typing import List, Dict, Any
from collections.abc import Mapping
from pathlib import Path
import yaml
import log


class ConfigError(Exception):
    def __init__(self, message='Error applying configuration'):
        super().__init__(message)


class Alacritty:
    def __init__(self):
        self.base_path = Path().home() / '.config' / 'alacritty'
        if not self.base_path.exists():
            raise ConfigError('Alacritty directory not found')

        self.config_file = self.base_path / 'alacritty.yml'
        if not self.config_file.exists():
            raise ConfigError('Alacritty config file not found')

        self.config = self._load(self.config_file)
        if self.config is None:
            self.config = {}
            log.warn('Alacritty config file was empty')

    def _load(self, yaml_file: Path) -> Dict[str, Any]:
        with open(yaml_file) as f:
            try:
                return yaml.load(f, Loader=yaml.FullLoader)
            except yaml.YAMLError as e:
                raise ConfigError((
                    'YAML error at parsing file "{0}", '
                    'at line {1.problem_mark.line}, '
                    'column {1.problem_mark.column}:\n'
                    '{1.problem} {1.context}'
                ).format(yaml_file.name, e))

    def save(self):
        with open(self.config_file,  'w') as f:
            yaml.dump(self.config, f)

    def apply(self, **config):
        if config is None or len(config) < 1:
            raise ConfigError('No options provided')

        actions = {
            'theme': self.change_theme,
            'font': self.change_font,
            'size': self.change_font_size,
            'opacity': self.change_opacity,
            'padding': self.change_padding,
            'list': self.list,
        }

        errors_found = 0
        for param, action in actions.items():
            if param in config:
                try:
                    action(config[param])
                except ConfigError as e:
                    log.err(e)
                    errors_found += 1

        if errors_found > 0:
            raise ConfigError(f'\n{errors_found} errors found')

    def change_theme(self, name: str):
        themes_directory = self.base_path / 'themes'
        if not themes_directory.exists():
            raise ConfigError(f'Themes directory not found')

        theme_file = themes_directory / f'{name}.yaml'
        if not theme_file.exists():
            raise ConfigError(f'Theme {name} not found')

        theme_yaml = self._load(theme_file)
        if theme_yaml is None:
            raise ConfigError(f'File {theme_file.name} is empty')
        if 'colors' not in theme_yaml:
            raise ConfigError(f'{theme_file} does not contain color config')

        expected_colors = [
            'black',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
        ]

        expected_props = {
            'primary': ['background', 'foreground'],
            'normal': expected_colors,
            'bright': expected_colors,
        }

        for k in expected_props:
            if k not in theme_yaml['colors']:
                log.warn(f'Missing "colors:{k}" for theme "{name}"')
                continue
            for v in expected_props[k]:
                if v not in theme_yaml['colors'][k]:
                    log.warn(f'Missing "colors:{k}:{v}" for theme "{name}"')

        self.config['colors'] = theme_yaml['colors']
        log.ok(f'Theme {name} applied')

    def change_font_size(self, size: float):
        if size <= 0:
            raise ConfigError('Font size cannot be negative or zero')

        if 'font' not in self.config:
            self.config['font'] = {}
            log.warn('"font" prop config was not present in alacritty.yml')
        self.config['font']['size'] = size
        log.ok(f'Font size set to {size:.1f}')

    def change_font(self, font: str):
        if 'font' not in self.config:
            self.config['font'] = {}
            log.warn('"font" prop was not present in alacritty.yml')

        fonts_file = self.base_path / 'fonts.yaml'
        if not fonts_file.exists():
            raise ConfigError('Fonts config file not found')

        fonts = self._load(fonts_file)
        if fonts is None:
            raise ConfigError(f'File {fonts_file.name} is empty')
        if 'fonts' not in fonts:
            raise ConfigError(f'No font config found in {fonts_file}')

        if font not in fonts['fonts']:
            raise ConfigError(f'Config for font "{font}" not found')

        font_types = ['normal', 'bold', 'italic']

        if isinstance(fonts['fonts'][font], str):
            font_name = fonts['fonts'][font]
            fonts['fonts'][font] = {}
            for t in font_types:
                fonts['fonts'][font][t] = font_name

        if not isinstance(fonts['fonts'][font], Mapping):
            raise ConfigError(f'Font {font} has wrong format')

        for t in font_types:
            if t not in fonts['fonts'][font]:
                raise ConfigError(f'Font {font} does not have "{t}" property')
            if t not in self.config['font']:
                self.config['font'][t] = {'family': 'tmp'}
            self.config['font'][t]['family'] = fonts['fonts'][font][t]

        log.ok(f'Font {font} applied')

    def change_opacity(self, opacity: float):
        if opacity < 0.0 or opacity > 1.0:
            raise ConfigError('Opacity should be between 0.0 and 1.0')

        self.config['background_opacity'] = opacity
        log.ok(f'Opacity set to {opacity:.2f}')

    def change_padding(self, padding: List[int]):
        if len(padding) != 2:
            raise ConfigError('Padding should only have an x and y value')

        x, y = padding
        if 'window' not in self.config:
            self.config['window'] = {}
            log.warn('"window" prop was not present in config file')
        if 'padding' not in self.config['window']:
            self.config['window']['padding'] = {}
            log.warn('"padding" prop was not present in config file')

        self.config['window']['padding']['x'] = x
        self.config['window']['padding']['y'] = y
        log.ok(f'Padding set to x: {x}, y: {y}')

    def list(self, to_be_listed: str):
        def list_themes():
            themes_dir = self.base_path / 'themes'
            if not themes_dir.is_dir():
                raise ConfigError('Cannot list themes, directory not found')

            themes = [file.name.split('.')[0] for file in themes_dir.iterdir()]
            if len(themes) < 1:
                log.warn('Themes directory is empty, cannot list themes')
            else:
                log.color_print('Themes:', log.Color.BOLD)
                for theme in themes:
                    log.color_print(f'    {theme}', log.Color.BLUE)

        def list_fonts():
            fonts_file = self.base_path / 'fonts.yaml'
            if not fonts_file.is_file():
                raise ConfigError('Cannot list fonts, fonts.yaml not found')

            fonts = self._load(fonts_file)
            if fonts is None or 'fonts' not in fonts:
                log.warn('Cannot list fonts, no fonts found')
            else:
                log.color_print('Fonts:', log.Color.BOLD)
                for font in fonts['fonts']:
                    log.color_print(f'    {font}', log.Color.PURPLE)

        options = {
            'themes': list_themes,
            'fonts': list_fonts,
        }

        if to_be_listed == 'all':
            for _, list_function in options.items():
                list_function()
        else:
            if to_be_listed not in options:
                raise ConfigError(f'Cannot list {to_be_listed}, unknown option')
            options[to_be_listed]()
