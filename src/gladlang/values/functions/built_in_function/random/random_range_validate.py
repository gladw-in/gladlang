"""Argument validation for RANDOM_RANGE: argument_count, type, and finiteness checks."""

import math

from gladlang.core.errors import RuntimeError
from gladlang.values.primitives.number import Number


class BuiltInFunctionRandomRangeValidate:
    __slots__ = ()

    def _validate_random_range_arguments(self, arguments, call_context):
        if len(arguments) != 2:
            return (
                None,
                None,
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "RANDOM_RANGE expects two arguments (start, stop)",
                    call_context,
                ),
            )

        first_argument, second_argument = arguments[0], arguments[1]
        if not isinstance(first_argument, Number) or not isinstance(
            second_argument, Number
        ):
            return (
                None,
                None,
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "Both arguments to RANDOM_RANGE must be Numbers",
                    call_context,
                ),
            )

        for value in (first_argument.value, second_argument.value):
            if isinstance(value, float) and not math.isfinite(value):
                return (
                    None,
                    None,
                    RuntimeError(
                        self.position_start,
                        self.position_end,
                        "Arguments to RANDOM_RANGE must be finite numbers (not inf or nan)",
                        call_context,
                    ),
                )

        try:
            start = int(first_argument.value)
            stop = int(second_argument.value)
        except (ValueError, TypeError, OverflowError):
            return (
                None,
                None,
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "Arguments to RANDOM_RANGE must be convertible to integers",
                    call_context,
                ),
            )

        if start >= stop:
            return (
                None,
                None,
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "start must be less than stop",
                    call_context,
                ),
            )

        return start, stop, None
