"""PRINTF output builder – processes the format string."""


class BuiltInFunctionPrintfCoreBuildOutput:
    __slots__ = ()

    def _build_printf_output(self, format_string, argument_values, call_context):
        output_parts = []
        output_length = 0
        index = 0
        position = 0
        format_length = len(format_string)

        while position < format_length:
            if format_string[position] == "%" and position + 1 < format_length:
                cursor = position + 1

                if format_string[cursor] == "%":
                    output_length, error = self._append_printf_text(
                        output_parts, output_length, "%", call_context
                    )

                    if error:
                        return None, error

                    position = cursor + 1
                    continue

                precision, cursor, error = self._parse_printf_precision(
                    format_string, cursor, format_length, call_context
                )

                if error:
                    return None, error

                formatted_text, index, error = self._handle_printf_specifier(
                    format_string,
                    position,
                    cursor,
                    format_length,
                    index,
                    argument_values,
                    precision,
                    call_context,
                )

                if error:
                    return None, error

                output_length, error = self._append_printf_text(
                    output_parts, output_length, formatted_text, call_context
                )

                if error:
                    return None, error

                position = cursor + 1
            else:
                output_length, error = self._append_printf_text(
                    output_parts, output_length, format_string[position], call_context
                )

                if error:
                    return None, error

                position += 1

        return "".join(output_parts), None
