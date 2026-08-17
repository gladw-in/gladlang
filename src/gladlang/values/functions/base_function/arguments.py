"""Argument-count checking and binding into a new call context."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult


class BaseFunctionArguments:
    __slots__ = ()

    def check_arguments(self, argument_names, arguments, calling_context=None):
        result = RuntimeResult()
        if len(arguments) != len(argument_names):
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    f"Incorrect argument count for '{self.name}'. Expected {len(argument_names)}, got {len(arguments)}",
                    calling_context or self.context,
                )
            )

        return result.success(None)

    def populate_arguments(self, argument_names, arguments, new_context):
        for index in range(len(arguments)):
            new_context.symbol_table.set(argument_names[index], arguments[index])

    def check_and_populate_arguments(self, argument_names, arguments, new_context):
        result = RuntimeResult()

        if argument_names is None:
            return result.success(None)

        if len(arguments) != len(argument_names):
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    f"Incorrect argument count for '{self.name}'. Expected {len(argument_names)}, got {len(arguments)}",
                    new_context,
                )
            )

        self.populate_arguments(argument_names, arguments, new_context)

        return result.success(None)
