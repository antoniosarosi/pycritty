import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock
from pycritty.api.ls import list_fonts, list_dir, list_themes, list_configs
from pycritty.resources.resource import ConfigFile, ConfigDir
from pycritty import PycrittyError


class TestListFonts:
    def test_it_should_raise_pycritty_error_when_file_does_not_exist(self):
        target_file = Mock(
            spec=ConfigFile,
            path=Path().cwd() / "example.yaml",
            exists=Mock(return_value=False),
        )

        with pytest.raises(PycrittyError):
            list_fonts(target_file)

    @pytest.mark.parametrize("fonts_content", [None, {}])
    @patch("pycritty.api.ls.yaml_io")
    def test_it_should_return_empty_fonts_when_file_has_no_content(
        self, mock_yaml_io: MagicMock, fonts_content
    ):
        target_file = Mock(
            spec=ConfigFile,
            path=Path().cwd() / "example.yaml",
            exists=Mock(return_value=True),
        )
        mock_yaml_io.read.return_value = fonts_content

        fonts = list_fonts(target_file)

        mock_yaml_io.read.assert_called_once_with(target_file)
        assert list(fonts) == []

    @patch("pycritty.api.ls.yaml_io")
    def test_it_should_return_fonts(self, mock_yaml_io: MagicMock):
        target_file = Mock(
            spec=ConfigFile,
            path=Path().cwd() / "example.yaml",
            exists=Mock(return_value=True),
        )
        mock_yaml_io.read.return_value = {
            "fonts": {"onedark": "OneDark", "cascadia": "Cascadia"}
        }

        fonts = list_fonts(target_file)

        mock_yaml_io.read.assert_called_once_with(target_file)
        assert list(fonts) == ["onedark", "cascadia"]


class TestListFiles:
    def test_it_should_list_files_from_directory(self):
        file_example_1 = Mock(stem="file1")
        file_example_2 = Mock(stem="file2")
        target_dir = Mock(
            spec=ConfigDir,
            path=Mock(iterdir=Mock(return_value=[file_example_1, file_example_2])),
        )

        files = list_dir(target_dir)

        assert files == ["file1", "file2"]

    def test_it_should_list_themes_files(self):
        file_example_1 = Mock(stem="file1")
        file_example_2 = Mock(stem="file2")
        target_dir = Mock(
            spec=ConfigDir,
            path=Mock(iterdir=Mock(return_value=[file_example_1, file_example_2])),
            exists=Mock(return_value=True),
        )

        files = list_themes(target_dir)

        assert files == ["file1", "file2"]

    def test_it_should_raise_pycritty_error_when_themes_dir_does_not_exist(self):
        target_dir = Mock(
            spec=ConfigDir,
            path=Path().cwd() / "example_dir",
            exists=Mock(return_value=False),
        )

        with pytest.raises(PycrittyError):
            list_themes(target_dir)

    def test_it_should_list_config_files(self):
        file_example_1 = Mock(stem="file1")
        file_example_2 = Mock(stem="file2")
        target_dir = Mock(
            spec=ConfigDir,
            path=Mock(iterdir=Mock(return_value=[file_example_1, file_example_2])),
            exists=Mock(return_value=True),
        )

        files = list_configs(target_dir)

        assert files == ["file1", "file2"]

    def test_it_should_raise_pycritty_error_when_config_dir_does_not_exist(self):
        target_dir = Mock(
            spec=ConfigDir,
            path=Path().cwd() / "example_dir",
            exists=Mock(return_value=False),
        )

        with pytest.raises(PycrittyError):
            list_configs(target_dir)
