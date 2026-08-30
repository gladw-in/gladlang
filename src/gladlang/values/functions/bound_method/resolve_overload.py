"""Resolves a FunctionGroup (overload set) to the variant matching the call's argument_count."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.functions.function_group import FunctionGroup


class BoundMethodResolveOverload:
    __slots__ = ()

    def _resolve_overload(self, current_function, current_arguments):
        if not isinstance(current_function, FunctionGroup):
            return current_function, None

        argument_count = len(current_arguments)
        if argument_count in current_function.functions:
            return current_function.functions[argument_count], None

        return None, RuntimeResult().failure(
            RuntimeError(
                current_function.position_start,
                current_function.position_end,
                f"No variant of function '{current_function.name}' accepts {argument_count} arguments",
                self.context,
            )
        )
