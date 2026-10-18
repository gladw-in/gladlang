"""Built-ins: INPUT (reads a line from stdin) and STR (string conversion)."""

import sys

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.string import String


class BuiltInFunctionInputString:
    __slots__ = ()

    def _execute_input(self, arguments, call_context):
        result = RuntimeResult()
        if len(arguments) > 1:
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "INPUT takes at most 1 argument",
                    call_context,
                )
            )

        prompt = ""
        if len(arguments) == 1:
            prompt = str(arguments[0])

        if prompt:
            sys.stdout.write(prompt)
            sys.stdout.flush()

        input_text = sys.stdin.readline(Settings.MAX_STRING_SIZE + 2)
        if input_text == "":
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "INPUT: end of file reached (no input available)",
                    call_context,
                )
            )

        input_text = input_text.rstrip("\r\n")

        if len(input_text) > Settings.MAX_STRING_SIZE:
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    f"INPUT exceeds maximum allowed size "
                    f"({Settings.MAX_STRING_SIZE:,} chars)",
                    call_context,
                )
            )

        return result.success(String(input_text))

    def _execute_str(self, arguments, call_context, calling_context):
        result = RuntimeResult()
        result.register(
            self.check_arguments(["value"], arguments, calling_context=calling_context)
        )

        if result.error:
            return result

        value = arguments[0]

        if isinstance(value, String):
            string_value = value.value
        else:
            string_value = str(value)

        if len(string_value) > Settings.MAX_STRING_SIZE:
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    f"STR result exceeds maximum allowed size "
                    f"({Settings.MAX_STRING_SIZE:,} chars)",
                    call_context,
                )
            )

        return result.success(String(string_value))
