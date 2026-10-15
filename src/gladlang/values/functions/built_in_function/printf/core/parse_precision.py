"""PRINTF precision parsing."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings


class BuiltInFunctionPrintfCoreParsePrecision:
    __slots__ = ()

    def _parse_printf_precision(
        self, format_string, cursor, format_length, call_context
    ):
        precision = None
        if format_string[cursor] == ".":
            cursor += 1
            precision_start = cursor
            while cursor < format_length and format_string[cursor].isdigit():
                cursor += 1

            precision_digits = format_string[precision_start:cursor]

            if not precision_digits:
                return (
                    None,
                    cursor,
                    RuntimeError(
                        self.position_start,
                        self.position_end,
                        "Expected digits after '.' in format specifier",
                        call_context,
                    ),
                )

            if (
                len(precision_digits) > 15
                or int(precision_digits) > Settings.MAX_PRINTF_PRECISION
            ):
                return (
                    None,
                    cursor,
                    RuntimeError(
                        self.position_start,
                        self.position_end,
                        f"PRINTF precision exceeds the maximum allowed "
                        f"precision ({Settings.MAX_PRINTF_PRECISION})",
                        call_context,
                    ),
                )

            precision = int(precision_digits)

        return precision, cursor, None
