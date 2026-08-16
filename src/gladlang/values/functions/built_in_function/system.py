"""System built-in functions – DELAY."""

import math
import time

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number


class BuiltInFunctionSystem:
    __slots__ = ()

    def _execute_delay(self, arguments, call_context, calling_context):
        result = RuntimeResult()
        if len(arguments) != 1:
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "DELAY expects one argument (seconds)",
                    call_context,
                )
            )

        delay_value = arguments[0]
        if not isinstance(delay_value, Number):
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "Argument to DELAY must be a Number",
                    call_context,
                )
            )

        try:
            sleep_seconds = float(delay_value.value)
        except (ValueError, TypeError, OverflowError):
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "DELAY argument must be a valid finite number",
                    call_context,
                )
            )

        if not math.isfinite(sleep_seconds):
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "DELAY argument must be a finite number (not inf or nan)",
                    call_context,
                )
            )

        if sleep_seconds < 0:
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "DELAY argument must not be negative",
                    call_context,
                )
            )

        if sleep_seconds > Settings.MAX_DELAY_SECONDS:
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    f"DELAY argument ({sleep_seconds:g} seconds) exceeds the maximum allowed "
                    f"delay ({Settings.MAX_DELAY_SECONDS:g} seconds)",
                    call_context,
                )
            )

        try:
            time.sleep(sleep_seconds)
        except OSError:
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "DELAY failed due to a system error",
                    call_context,
                )
            )

        return result.success(Number.null.copy())
