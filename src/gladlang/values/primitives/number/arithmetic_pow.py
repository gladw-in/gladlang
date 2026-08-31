"""Number arithmetic: exponentiation, with overflow/domain guards."""

import math

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings


class NumberArithmeticPow:
    __slots__ = ()

    def powed_by(self, other):
        from gladlang.values.primitives.number import Number

        if isinstance(other, Number):
            exponent = other.value
            if exponent > Settings.MAX_EXPONENT:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Exponent too large (limit: 1000)",
                    self.context,
                )

            base = self.value
            if (
                isinstance(base, int)
                and base.bit_length() > Settings.MAX_BASE_BITS_FOR_EXPONENT
                and exponent > 2
            ):
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Base too large for exponentiation",
                    self.context,
                )

            try:
                result = self.value**other.value
            except (ValueError, ZeroDivisionError, OverflowError) as exception:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    str(exception),
                    self.context,
                )

            if isinstance(result, complex):
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Math domain error: result is complex",
                    self.context,
                )

            if isinstance(result, float) and math.isnan(result):
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Math domain error: result is NaN",
                    self.context,
                )

            if isinstance(result, float) and math.isinf(result):
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Arithmetic result is infinite (float overflow)",
                    self.context,
                )

            return Number(result).set_context(self.context), None

        return None, self._illegal(other)
