"""Number subtraction."""

import math

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings


class NumberArithmeticAddSubtractMulSubtract:
    __slots__ = ()

    def subbed_by(self, other):
        if hasattr(other, "_is_null") and other._is_null:
            return None, self._illegal(other)

        from gladlang.values.primitives.number import Number

        if isinstance(other, Number):
            try:
                result = self.value - other.value
            except OverflowError:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Arithmetic result is infinite (float overflow)",
                    self.context,
                )

            if isinstance(result, int) and result.bit_length() > Settings.MAX_INT_BITS:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Arithmetic result too large (exceeds integer size limit)",
                    self.context,
                )

            if isinstance(result, float) and not math.isfinite(result):
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    (
                        "Arithmetic result is infinite (float overflow)"
                        if math.isinf(result)
                        else "Arithmetic result is not finite"
                    ),
                    self.context,
                )

            return Number(result).set_context(self.context), None

        return None, self._illegal(other)
