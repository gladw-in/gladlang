"""RANDOM built-in function – cryptographically secure 32-bit integer."""

import secrets

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number


class BuiltInFunctionRandomInt:
    __slots__ = ()

    def _execute_random(self, arguments, call_context, calling_context):
        result = RuntimeResult()
        if len(arguments):
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "RANDOM takes no arguments",
                    call_context,
                )
            )

        return result.success(Number(secrets.randbits(32)))
