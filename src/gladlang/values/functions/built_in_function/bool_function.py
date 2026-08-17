"""Built-in: BOOL (truthiness conversion)."""

from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number


class BuiltInFunctionBool:
    __slots__ = ()

    def _execute_bool(self, arguments, call_context, calling_context):
        result = RuntimeResult()
        result.register(
            self.check_arguments(["value"], arguments, calling_context=calling_context)
        )

        if result.error:
            return result

        return result.success(Number(1) if arguments[0].is_true() else Number(0))
