"""RANDOM_FLOAT built-in function – cryptographically secure float in [0, 1)."""

import secrets

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number


class BuiltInFunctionRandomFloat:
    __slots__ = ()

    def _execute_random_float(self, arguments, call_context, calling_context):
        result = RuntimeResult()
        if len(arguments):
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "RANDOM_FLOAT takes no arguments",
                    call_context,
                )
            )

        return result.success(Number(secrets.randbelow(10**16) / 10**16))
