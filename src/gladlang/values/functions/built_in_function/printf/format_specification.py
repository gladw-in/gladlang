"""Formats a single PRINTF conversion specifier (%s, %d, %f) for one argument."""

import math

from gladlang.core.errors import RuntimeError
from gladlang.values.primitives.number import Number


class BuiltInFunctionPrintfFormatSpecification:
    __slots__ = ()

    def _format_printf_specification(
        self, format_specification, argument_value, precision, call_context
    ):
        if format_specification == "s":
            if precision is not None:
                return None, RuntimeError(
                    self.position_start,
                    self.position_end,
                    "Precision is not supported for '%s'",
                    call_context,
                )

            return str(argument_value), None

        if format_specification == "d":
            if precision is not None:
                return None, RuntimeError(
                    self.position_start,
                    self.position_end,
                    "Precision is not supported for '%d'",
                    call_context,
                )

            return self._format_printf_int_specification(argument_value, call_context)

        if format_specification == "f":
            return self._format_printf_float_specification(
                argument_value, precision, call_context
            )

        return None, RuntimeError(
            self.position_start,
            self.position_end,
            f"Unsupported format specifier '%{format_specification}'",
            call_context,
        )

    def _format_printf_int_specification(self, argument_value, call_context):
        if not isinstance(argument_value, Number):
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                f"Expected Number for '%d', got {type(argument_value).__name__}",
                call_context,
            )

        if isinstance(argument_value.value, float) and not math.isfinite(
            argument_value.value
        ):
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                f"Cannot format non-finite value {argument_value} as integer for '%d'",
                call_context,
            )

        try:
            return str(int(argument_value.value)), None
        except (ValueError, TypeError, OverflowError):
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                f"Cannot format value {argument_value} as integer for '%d'",
                call_context,
            )

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
