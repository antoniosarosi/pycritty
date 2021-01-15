from typing import List
from pathlib import Path
from ..io import log


class Resource:
    """Wrapper around Path used for managing config files and directories"""

    def __init__(self, resource_path: Path):
        self.path = resource_path

    def exists(self) -> bool:
        return self.path.exists()

    def create(self):
        self.path.touch()

    def get_or_create(self) -> Path:
        if not self.exists():
            log.warn('Created missing resource =>', log.Color.BLUE, str(self.path))
            self.create()

        return self.path

    def __str__(self):
        return str(self.path)


class ConfigDir(Resource):
    """Directory containing config files"""

    def exists(self) -> bool:
        return self.path.is_dir()

    def create(self):
        self.path.mkdir(parents=True, exist_ok=True)


class ConfigFile(Resource):
    """Class used to manage config files that may have many possible extensions"""

    YAML = ['yml', 'yaml']

    def __init__(self, parent: Path, name: str, extensions: List[str]):
        if len(extensions) > 0:
            default_path = parent / f'{name}.{extensions[0]}'
        else:
            default_path = parent / name
        super().__init__(default_path)
        self.parent = parent
        self.name = name
        self.extensions = extensions

        self.possible_files = self._match_path()
        if len(self.possible_files) >= 1:
            self.path = self.possible_files[0]

    def _match_path(self) -> List[Path]:
        files_found = []
        for ext in self.extensions:
            file = self.parent / f'{self.name}.{ext}'
            if file.is_file():
                files_found.append(file)

        return files_found

    def exists(self) -> bool:
        if len(self.possible_files) > 1:
            log.warn(
                'Found some files with the same name but different extensions:',
                log.Color.BLUE,
                *map(lambda f: f'    {f}', self.possible_files),
                sep='\n',
            )
            log.warn('Defaulting to =>', log.Color.PURPLE, self.path)

        return self.path.is_file()

    def create(self):
        self.path.touch()
