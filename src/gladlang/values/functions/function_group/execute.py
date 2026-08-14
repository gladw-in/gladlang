"""Dispatches a call to the overload variant matching the given argument_count."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult


class FunctionGroupExecute:
    __slots__ = ()

    def execute(self, arguments, interpreter, calling_context=None):
        argument_count = len(arguments)
        if argument_count not in self.functions:
            return RuntimeResult().failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    f"No variant of function '{self.name}' found that accepts {argument_count} arguments",
                    self.context,
                )
            )

        selected_function = self.functions[argument_count]
        selected_function.set_position(self.position_start, self.position_end)

        return selected_function.execute(arguments, interpreter, calling_context)
