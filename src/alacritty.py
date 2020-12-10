# Alacritty config options
# Antonio Sarosi
# December 10, 2020

from typing import List, Dict
from collections.abc import Mapping
from pathlib import Path
import yaml


class ConfigError(Exception):
    def __init__(self, message='Error applying configuration'):
        super().__init__(message)


class Alacritty:
    def __init__(self):
        self.base_path = Path().home() / '.config' / 'alacritty'
        if not self.base_path.exists():
            raise ConfigError(f'Alacritty directory not found')

        self.config_file = self.base_path / 'alacritty.yml'
        if not self.config_file.exists():
            raise ConfigError(f'Alacritty config file not found')

        self.config = self._load(self.config_file)
        if self.config is None:
            self.config = {}

    def _load(self, yaml_file: Path) -> Dict[str, any]:
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
        }

        for param, action in actions.items():
            if param in config:
                action(config[param])

    def change_theme(self, theme: str):
        themes_directory = self.base_path / 'themes'
        if not themes_directory.exists():
            raise ConfigError(f'Themes directory not found')

        theme_file = themes_directory / f'{theme}.yaml'
        if not theme_file.exists():
            raise ConfigError(f'Theme {theme} not found')

        theme = self._load(theme_file)
        if theme is None:
            raise ConfigError(f'File {theme_file.name} is empty')
        if 'colors' not in theme:
            raise ConfigError(f'{theme_file} does not contain color config')

        self.config['colors'] = theme['colors']

    def change_font_size(self, size: float):
        if size <= 0:
            raise ConfigError('Font size cannot be negative or zero')

        if 'font' not in self.config:
            self.config['font'] = {}
        self.config['font']['size'] = size

    def change_font(self, font: str):
        if 'font' not in self.config:
            self.config['font'] = {}

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

    def change_opacity(self, opacity: float):
        if opacity < 0.0 or opacity > 1.0:
            raise ConfigError('Opacity should be between 0.0 and 1.0')

        self.config['background_opacity'] = opacity

    def change_padding(self, padding: List[int]):
        if len(padding) != 2:
            raise ConfigError('Padding should only have an x and y value')

        x, y = padding
        if 'window' not in self.config:
            self.config['window'] = {}
        if 'padding' not in self.config['window']:
            self.config['window']['padding'] = {}

        self.config['window']['padding']['x'] = x
        self.config['window']['padding']['y'] = y
