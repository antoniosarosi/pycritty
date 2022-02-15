from typing import Dict, Callable, Any
from collections.abc import Mapping
from pycritty import resources, PycrittyError
from pycritty.io import log, yaml_io


class ConfigError(PycrittyError):
    def __init__(self, message='Error applying configuration'):
        super().__init__(message)


class Config:
    """Applies changes to the config

    >>> conf = Config()
    >>> conf.change_theme('dracula')
    >>> conf.change_font('UbuntuMono')
    >>> conf.apply()
    """

    def __init__(self):
        self.config = yaml_io.read(resources.config_file.get_or_create())
        if self.config is None:
            self.config = {}

    def apply(self):
        yaml_io.write(self.config, resources.config_file)

    def set(self, **kwargs):
        """Set multiple changes at once

        >>> conf = SetConfig()
        >>> conf.set(theme='onedark', font='UbuntuMono', font_size=14, opacity=1)
        >>> conf.apply()
        """
        options: Dict[str, Callable[[Any], Any]] = {
            'theme': self.change_theme,
            'font': self.change_font,
            'font_size': self.change_font_size,
            'offset': self.change_font_offset,
            'padding': self.change_padding,
            'opacity': self.change_opacity,
        }

        errors = 0

        for opt, arg in kwargs.items():
            if opt in options:
                try:
                    options[opt](arg)
                except PycrittyError as e:
                    log.err(e)
                    errors += 1

        if errors > 0:
            raise ConfigError('\nFailed applying some settings')
        

    def change_theme(self, theme: str):
        theme_file = resources.get_theme(theme)
        if not theme_file.exists():
            raise PycrittyError(f'Theme "{theme}" not found')

        theme_yaml = yaml_io.read(theme_file)
        if theme_yaml is None:
            raise ConfigError(f'File {theme_file} is empty')
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
                log.warn(f'Missing "colors:{k}" for theme "{theme}"')
                continue
            for v in expected_props[k]:
                if v not in theme_yaml['colors'][k]:
                    log.warn(f'Missing "colors:{k}:{v}" for theme "{theme}"')

        self.config['colors'] = theme_yaml['colors']
        log.ok(f'Theme {theme} applied')

    def change_font(self, font: str):
        if 'font' not in self.config:
            self.config['font'] = {}
            log.warn(f'"font" prop was not present in {resources.config_file}')

        fonts_file = resources.fonts_file.get_or_create()
        fonts = yaml_io.read(fonts_file)
        if fonts is None:
            raise ConfigError(
                f'Failed changing font, file "{fonts_file}" is empty'
            )
        if 'fonts' not in fonts:
            raise ConfigError(
                f'Could not change font, "font" config not found in {fonts_file}'
            )

        fonts = fonts['fonts']
        if font not in fonts:
            raise ConfigError(
                f'Config for font "{font}" not found in {fonts_file}'
            )

        font_types = ['normal', 'bold', 'italic']

        if isinstance(fonts[font], str):
            font_name = fonts[font]
            fonts[font] = {}
            for t in font_types:
                fonts[font][t] = font_name

        if not isinstance(fonts[font], Mapping):
            raise ConfigError(
                f'Font "{font}" has wrong format at file {fonts_file}'
            )

        for t in font_types:
            if t not in fonts[font]:
                raise ConfigError(f'Font "{font}" does not have "{t}" property')
            if t not in self.config['font']:
                self.config['font'][t] = {'family': 'tmp'}
            self.config['font'][t]['family'] = fonts[font][t]

        log.ok(f'Font {font} applied')

    def change_font_size(self, size: float):
        if size <= 0:
            raise ConfigError('Font size cannot be negative or zero')

        if 'font' not in self.config:
            self.config['font'] = {}
            log.warn(f'"font" prop was not present in {resources.config_file}')
        self.config['font']['size'] = size
        log.ok(f'Font size set to {size:.1f}')

    def change_opacity(self, opacity: float):
        if opacity < 0.0 or opacity > 1.0:
            raise ConfigError('Opacity should be between 0.0 and 1.0')

        if 'window' not in self.config:
            self.config['window'] = {}
            log.warn(f'"window" prop was not present in {resources.config_file}')
        if 'opacity' not in self.config['window']:
            self.config['window']['opacity'] = {}
            log.warn(f'"opacity" prop was not present in {resources.config_file}')

        self.config['window']['opacity']  = opacity
        log.ok(f'Opacity set to {opacity:.2f}')

    def change_padding(self, padding=(1, 1)):
        if len(padding) != 2:
            raise ConfigError('Padding should only have an x and y value')

        x, y = padding
        if 'window' not in self.config:
            self.config['window'] = {}
            log.warn(f'"window" prop was not present in {resources.config_file}')
        if 'padding' not in self.config['window']:
            self.config['window']['padding'] = {}
            log.warn(f'"padding" prop was not present in {resources.config_file}')

        self.config['window']['padding']['x'] = x
        self.config['window']['padding']['y'] = y
        log.ok(f'Padding set to x: {x}, y: {y}')

    def change_font_offset(self, offset=(0, 0)):
        if len(offset) != 2:
            raise ConfigError('Wrong offset format, should be (x, y)')

        x, y = offset
        if 'font' not in self.config:
            self.config['font'] = {}
        if 'offset' not in self.config['font']:
            log.warn('"offset" prop was not set')
            self.config['font']['offset'] = {}

        self.config['font']['offset']['x'] = x
        self.config['font']['offset']['y'] = y
        log.ok(f'Offset set to x: {x}, y: {y}')


def set_config(**kwargs):
    config = Config()
    try:
        config.set(**kwargs)
    finally:
        config.apply()
 