from unittest.mock import Mock
import pytest
from pycritty.cli.cli import Cli, cli
from pycritty import PycrittyError


class TestCli:
    def test_it_should_execute_pycritty_when_command_is_none(self):
        cli_test = Cli()
        mock_executable_command = Mock()
        cli_test.define_command(name="pycritty", action=mock_executable_command)

        cli_test.execute(command=None, args={})

        mock_executable_command.assert_called_once()

    def test_it_should_raise_pycritty_error_when_command_does_not_exist(self):
        cli_test = Cli()

        with pytest.raises(PycrittyError) as e:
            cli_test.execute(command="unknown_command", args={})
            assert e == "Unkown command unknown_command"

    def test_it_should_execute_command_with_args(self):
        cli_test = Cli()
        mock_executable_command = Mock()
        cli_test.define_command(name="example_command", action=mock_executable_command)

        cli_test.execute(command="example_command", args={"foo": 1, "bar": 2})

        mock_executable_command.assert_called_once_with(foo=1, bar=2)


@pytest.mark.parametrize(
    "API_command",
    [
        "pycritty",
        "ls",
        "rm",
        "save",
        "load",
        "install",
    ],
)
def test_validate_cli_API_commands(API_command):
    assert API_command in cli.commands
