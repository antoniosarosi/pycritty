from typing import Dict, Any
from .. import PycrittyError
from ..io import log


class Command:
    """Objects representing a CLI command or subcommand"""

    requires_args = False

    def execute(self, actions: Dict[str, Any]):
        """Execute the actions associted to this command.

        By default it will try to map each action to a method
        of this object and execute it with the given arguments.

        >>> # Example:
        >>> Command c = SomeSubclassCommand()
        >>> c.execute({'do_this', [1, 2, 3], 'then_do_this', 'foo'})
        >>> # Would result in:
        >>> c.do_this([1, 2, 3])
        >>> c.then_do_this('foo')

        This makes it easier to 'reference' the code that has
        to run from the CLI, but it cannot be used if the method
        requires more than one argument, unless using tuples
        or passing arguments manually.
        """

        errors = 0
        for method, args in actions.items():
            call = getattr(self, method)
            try:
                if args is None:
                    call()
                else:
                    call(args)
            except PycrittyError as e:
                log.err(e)
                errors += 1

        self.apply()

        if errors > 0:
            raise PycrittyError(f'\n{errors} error(s) found')

    def apply(self):
        """Some commands might need to dump data to config files or run
        code after all actions have been performed.
        """
        pass
