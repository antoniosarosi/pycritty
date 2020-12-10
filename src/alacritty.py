from pathlib import Path
from collections.abc import Mapping
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

    def _load(self, yaml_file: Path):
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

    def apply(self):
        with open(self.config_file,  'w') as f:
            yaml.dump(self.config, f)
        # print(yaml.dump(self.config))

    def change_theme(self, theme: str):
        if theme is None:
            return

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

    def change_font(self, font: str = None, size: float = None):
        if 'font' not in self.config:
            self.config['font'] = {}
        if size is not None:
            self.config['font']['size'] = size

        if font is None:
            return

        fonts_file = self.base_path / 'fonts.yaml'
        if not fonts_file.exists():
            raise ConfigError('Fonts config file not found')

        fonts = self._load(fonts_file)
        if fonts is None:
            raise ConfigError(f'File {fonts_file.name} is empty')
        if 'fonts' not in fonts:
            raise ConfigError(f'No font config found in {fonts_file}')

        fonts = fonts['fonts']
        if font not in fonts:
            raise ConfigError(f'Config for font "{font}" not found')

        font_types = ['normal', 'bold', 'italic']

        if isinstance(fonts[font], str):
            font_name = fonts[font]
            fonts[font] = {}
            for t in font_types:
                fonts[font][t] = font_name

        if not isinstance(fonts[font], Mapping):
            raise ConfigError(f'Font {font} has wrong format')

        for t in font_types:
            if t not in fonts[font]:
                raise ConfigError(f'Font {font} does not have "{t}" property')

        for t in font_types:
            self.config['font'][t]['family'] = fonts[font][t]

    def change_opacity(self, opacity=1.0):
        if opacity is None:
            return
        if opacity > 1.0 or opacity < 0:
            raise ConfigError('Opacity should be between 0.0 and 1.0')

        self.config['background_opacity'] = opacity
        
    def change_padding(self, x: float, y: float):
        if 'window' not in self.config:
            self.config['window'] = {}
        if 'padding' not in self.config['window']:
            self.config['window']['padding'] = {}

        self.config['window']['padding']['x'] = x
        self.config['window']['padding']['y'] = y
