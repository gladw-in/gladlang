"""PRINTF format specifier handling."""

from gladlang.core.errors import RuntimeError


class BuiltInFunctionPrintfCoreHandleSpecifier:
    __slots__ = ()

    def _handle_printf_specifier(
        self,
        format_string,
        position,
        cursor,
        format_length,
        index,
        argument_values,
        precision,
        call_context,
    ):
        if cursor >= format_length:
            return (
                None,
                index,
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "Format specifier is missing a type character (e.g. 's', 'd', 'f')",
                    call_context,
                ),
            )

        format_specification = format_string[cursor]
        full_specifier = format_string[position + 1 : cursor + 1]

        if index >= len(argument_values):
            return (
                None,
                index,
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    f"Not enough arguments for format specifier '%{full_specifier}'",
                    call_context,
                ),
            )

        argument_value = argument_values[index]
        index += 1

        formatted_text, specification_error = self._format_printf_specification(
            format_specification, argument_value, precision, call_context
        )

        if specification_error:
            return None, index, specification_error

        return formatted_text, index, None
