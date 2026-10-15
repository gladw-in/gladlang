"""Dispatches a single PRINTF conversion specifier."""

from gladlang.core.errors import RuntimeError


class BuiltInFunctionPrintfFormatSpecificationCore:
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
