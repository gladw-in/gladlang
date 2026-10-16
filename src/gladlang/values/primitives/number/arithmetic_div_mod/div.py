"""Division (/) for numbers."""

import math

from gladlang.core.errors import RuntimeError


class NumberArithmeticDiv:
    __slots__ = ()

    def dived_by(self, other):
        if hasattr(other, "_is_null") and other._is_null:
            return None, self._illegal(other)

        from gladlang.values.primitives.number import Number

        if isinstance(other, Number):
            if not other.value:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Division by zero",
                    self.context,
                )

            try:
                result = self.value / other.value
            except OverflowError:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Division result exceeds float range; use integer floor division (//) instead",
                    self.context,
                )

            if math.isinf(result):
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Arithmetic result is infinite (float overflow)",
                    self.context,
                )

            return Number(result).set_context(self.context), None

        return None, self._illegal(other)
