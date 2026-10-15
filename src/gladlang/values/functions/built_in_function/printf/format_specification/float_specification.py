"""Formats a value for the PRINTF '%f' specifier."""

import math

from gladlang.core.errors import RuntimeError
from gladlang.values.primitives.number import Number


class BuiltInFunctionPrintfFormatSpecificationFloat:
    __slots__ = ()

    def _format_printf_float_specification(
        self, argument_value, precision, call_context
    ):
        if not isinstance(argument_value, Number):
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                f"Expected Number for '%f', got {type(argument_value).__name__}",
                call_context,
            )

        float_value = float(argument_value.value)

        if precision is None:
            return str(float_value), None

        if not math.isfinite(float_value):
            return str(float_value), None

        return format(float_value, f".{precision}f"), None
