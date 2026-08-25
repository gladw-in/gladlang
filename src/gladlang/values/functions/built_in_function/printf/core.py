"""PRINTF main loop – orchestrates validation, spec formatting, and output."""

import sys

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number


class BuiltInFunctionPrintfCore:
    __slots__ = ()

    def _execute_printf(self, arguments, call_context, calling_context):
        result = RuntimeResult()

        format_string, argument_values, error = self._validate_printf_arguments(
            arguments, call_context
        )
        if error:
            return result.failure(error)

        output_parts = []
        output_length = 0
        index = 0
        position = 0
        format_length = len(format_string)

        def _append(text):
            nonlocal output_length
            output_parts.append(text)
            output_length += len(text)
            return output_length <= Settings.MAX_STRING_SIZE

        def _output_too_large():
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    f"PRINTF output exceeds maximum allowed size ({Settings.MAX_STRING_SIZE:,} chars)",
                    call_context,
                )
            )

        while position < format_length:
            if format_string[position] == "%" and position + 1 < format_length:
                cursor = position + 1

                if format_string[cursor] == "%":
                    if not _append("%"):
                        return _output_too_large()

                    position = cursor + 1
                    continue

                precision = None
                if format_string[cursor] == ".":
                    cursor += 1
                    precision_start = cursor
                    while cursor < format_length and format_string[cursor].isdigit():
                        cursor += 1

                    precision_digits = format_string[precision_start:cursor]

                    if not precision_digits:
                        return result.failure(
                            RuntimeError(
                                self.position_start,
                                self.position_end,
                                "Expected digits after '.' in format specifier",
                                call_context,
                            )
                        )

                    if (
                        len(precision_digits) > 15
                        or int(precision_digits) > Settings.MAX_PRINTF_PRECISION
                    ):
                        return result.failure(
                            RuntimeError(
                                self.position_start,
                                self.position_end,
                                f"PRINTF precision exceeds the maximum allowed "
                                f"precision ({Settings.MAX_PRINTF_PRECISION})",
                                call_context,
                            )
                        )

                    precision = int(precision_digits)

                if cursor >= format_length:
                    return result.failure(
                        RuntimeError(
                            self.position_start,
                            self.position_end,
                            "Format specifier is missing a type character (e.g. 's', 'd', 'f')",
                            call_context,
                        )
                    )

                format_specification = format_string[cursor]
                full_specifier = format_string[position + 1 : cursor + 1]

                if index >= len(argument_values):
                    return result.failure(
                        RuntimeError(
                            self.position_start,
                            self.position_end,
                            f"Not enough arguments for format specifier '%{full_specifier}'",
                            call_context,
                        )
                    )

                argument_value = argument_values[index]
                index += 1

                formatted_text, specification_error = self._format_printf_specification(
                    format_specification, argument_value, precision, call_context
                )

                if specification_error:
                    return result.failure(specification_error)

                if not _append(formatted_text):
                    return _output_too_large()

                position = cursor + 1
            else:
                if not _append(format_string[position]):
                    return _output_too_large()

                position += 1

        sys.stdout.write("".join(output_parts))
        sys.stdout.flush()

        return result.success(Number.null.copy())
