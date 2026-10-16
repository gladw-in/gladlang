"""Modulo (%) for numbers."""

import math

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings


class NumberArithmeticMod:
    __slots__ = ()

    def modded_by(self, other):
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
                result = self.value % other.value
            except (OverflowError, ValueError):
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Invalid modulo operation",
                    self.context,
                )

            if isinstance(result, float) and not math.isfinite(result):
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Arithmetic result is not finite",
                    self.context,
                )

            if isinstance(result, int) and result.bit_length() > Settings.MAX_INT_BITS:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Arithmetic result too large (exceeds integer size limit)",
                    self.context,
                )

            return Number(result).set_context(self.context), None

        return None, self._illegal(other)
