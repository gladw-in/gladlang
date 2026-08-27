"""RANDOM_RANGE built-in function – cryptographically secure integer in [start, stop)."""

import secrets

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number


class BuiltInFunctionRandomRange:
    __slots__ = ()

    def _execute_random_range(self, arguments, call_context, calling_context):
        result = RuntimeResult()

        start, stop, error = self._validate_random_range_arguments(
            arguments, call_context
        )
        if error:
            return result.failure(error)

        range_size = stop - start
        if range_size.bit_length() > Settings.MAX_INT_BITS:
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "RANDOM_RANGE span (stop - start) exceeds the integer size limit",
                    call_context,
                )
            )

        return result.success(Number(start + secrets.randbelow(range_size)))
