"""Argument validation for PRINTF: argument_count and format-string type checks."""

from gladlang.core.errors import RuntimeError
from gladlang.values.primitives.string import String


class BuiltInFunctionPrintfValidate:
    __slots__ = ()

    def _validate_printf_arguments(self, arguments, call_context):
        if len(arguments) < 1:
            return (
                None,
                None,
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "PRINTF expects at least a format string",
                    call_context,
                ),
            )

        format_argument = arguments[0]
        if not isinstance(format_argument, String):
            return (
                None,
                None,
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "First argument to PRINTF must be a String",
                    call_context,
                ),
            )

        return format_argument.value, arguments[1:], None
