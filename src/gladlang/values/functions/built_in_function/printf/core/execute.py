"""PRINTF main execution entry point."""

import sys

from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number


class BuiltInFunctionPrintfCoreExecute:
    __slots__ = ()

    def _execute_printf(self, arguments, call_context, calling_context):
        result = RuntimeResult()

        format_string, argument_values, error = self._validate_printf_arguments(
            arguments, call_context
        )

        if error:
            return result.failure(error)

        output, error = self._build_printf_output(
            format_string, argument_values, call_context
        )

        if error:
            return result.failure(error)

        sys.stdout.write(output)
        sys.stdout.flush()

        return result.success(Number.null.copy())
