import setuptools
from setuptools.command.install import install
from pathlib import Path
from pycritty import __version__


class PostInstallHook(install):
    user_options = install.user_options + [
        ('themes=', None, 'Themes to be installed')
    ]

    def initialize_options(self):
        super().initialize_options()
        self.themes = None

    def finalize_options(self):
        super().finalize_options()

    def run(self):
        super().run()
        self.hook()

    def hook(self):
        config_path = Path(__file__).parent / 'config'
        alacirtty_path = Path().home() / '.config' / 'alacritty'
        if not alacirtty_path.is_dir():
            alacirtty_path.mkdir(parents=True)
        config_file = alacirtty_path / 'alacritty.yml'
        if not config_file.is_file():
            config_file.touch()
            
        theme_files = list((config_path / 'themes').iterdir())
        self.exclude = set(theme_files)
        if self.themes is not None:
            include = set(self.themes.replace(' ', '').split(','))
            if 'all' in include:
                include = set([f.name.split('.')[0] for f in theme_files])
            for f in theme_files:
                if f.name.split('.')[0] in include:
                    self.exclude.remove(f)
        self.cp(config_path, alacirtty_path)

    def cp(self, src_dir: Path, dest_dir: Path):
        for src_child in src_dir.iterdir():
            if src_child in self.exclude:
                continue
            dest_child = dest_dir / src_child.name
            if src_child.is_dir():
                if not dest_child.is_dir():
                    dest_child.mkdir()
                self.cp(src_child, dest_child)
            else:
                if not dest_child.is_file():
                    dest_child.touch()
                    with open(src_child, 'r') as s, open(dest_child, 'w') as d:
                        d.write(s.read())


with open("README.md", "r", encoding="utf-8") as f:
    README = f.read()

setuptools.setup(
    name="pycritty",
    version=__version__,
    author="Antonio Sarosi",
    author_email="sarosiantonio@gmail.com",
    description="CLI program that allows you to change your alacritty config file with one command.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/antoniosarosi/pycritty",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Terminals :: Terminal Emulators/X Terminals"
    ],
    keywords="alacritty",
    python_requires='>=3.6',
    install_requires=["PyYAML"],
    include_package_data=True,
    cmdclass={
        'install': PostInstallHook,
    },
    entry_points={
        "console_scripts": ["pycritty = pycritty.main:main"]
    },
)
