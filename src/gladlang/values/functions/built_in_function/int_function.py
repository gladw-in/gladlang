"""Built-in: INT numeric conversion."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number
from gladlang.values.primitives.string import String


class BuiltInFunctionInt:
    __slots__ = ()

    def _execute_int(self, arguments, call_context, calling_context):
        result = RuntimeResult()
        result.register(
            self.check_arguments(["value"], arguments, calling_context=calling_context)
        )
        if result.error:
            return result

        argument = arguments[0]

        if not isinstance(argument, (Number, String)):
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    f"Argument for INT must be a Number or String, got {type(argument).__name__}",
                    call_context,
                )
            )

        try:
            if isinstance(argument, Number):
                int_value = int(argument.value)
            else:
                try:
                    int_value = int(argument.value)
                except ValueError:
                    int_value = int(float(argument.value))

        except (ValueError, OverflowError):
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    f"Cannot convert '{argument.value}' to INT",
                    call_context,
                )
            )

        if int_value.bit_length() > Settings.MAX_INT_BITS:
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "INT: result too large (exceeds integer size limit)",
                    call_context,
                )
            )

        return result.success(Number(int_value))
