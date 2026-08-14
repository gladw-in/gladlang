"""Built-in: FLOAT numeric conversion."""

import math

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number
from gladlang.values.primitives.string import String


class BuiltInFunctionFloat:
    __slots__ = ()

    def _execute_float(self, arguments, call_context, calling_context):
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
                    f"Argument for FLOAT must be a Number or String, got {type(argument).__name__}",
                    call_context,
                )
            )

        try:
            float_value = float(argument.value)
        except ValueError:
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    f"Cannot convert '{argument.value}' to FLOAT",
                    call_context,
                )
            )

        if math.isinf(float_value) or math.isnan(float_value):
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    f"FLOAT: result is not a finite number (got '{argument.value}')",
                    call_context,
                )
            )

        return result.success(Number(float_value))
