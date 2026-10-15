"""Formats a value for the PRINTF '%d' specifier."""

import math

from gladlang.core.errors import RuntimeError
from gladlang.core.util.int_text import int_to_str
from gladlang.values.primitives.number import Number


class BuiltInFunctionPrintfFormatSpecificationInt:
    __slots__ = ()

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
            return int_to_str(int(argument_value.value)), None
        except (ValueError, TypeError, OverflowError):
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                f"Cannot format value {argument_value} as integer for '%d'",
                call_context,
            )
