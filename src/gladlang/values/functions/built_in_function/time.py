"""TIME built-in functions – TIME, TIME_SECONDS, TIME_MILLIS, and TIME_NANOS."""

import time

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number


class BuiltInFunctionTime:
    __slots__ = ()

    def _execute_time(self, arguments, call_context, calling_context):
        result = RuntimeResult()
        if len(arguments):
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "TIME takes no arguments",
                    call_context,
                )
            )

        return result.success(Number(time.time()))

    def _execute_time_seconds(self, arguments, call_context, calling_context):
        result = RuntimeResult()
        if len(arguments):
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "TIME_SECONDS takes no arguments",
                    call_context,
                )
            )

        return result.success(Number(time.time_ns() // 1_000_000_000))

    def _execute_time_millis(self, arguments, call_context, calling_context):
        result = RuntimeResult()
        if len(arguments):
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "TIME_MILLIS takes no arguments",
                    call_context,
                )
            )

        return result.success(Number(time.time_ns() // 1_000_000))

    def _execute_time_nanos(self, arguments, call_context, calling_context):
        result = RuntimeResult()
        if len(arguments):
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "TIME_NANOS takes no arguments",
                    call_context,
                )
            )

        return result.success(Number(time.time_ns()))
