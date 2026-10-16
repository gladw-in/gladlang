"""Number addition and string concatenation."""

import math

from gladlang.core.errors import RuntimeError
from gladlang.core.util.int_text import int_to_str
from gladlang.core.util.settings import Settings


class NumberArithmeticAddSubtractMulAdd:
    __slots__ = ()

    def added_to(self, other):
        if hasattr(other, "_is_null") and other._is_null:
            return None, self._illegal(other)

        from gladlang.values.primitives.number import Number

        if isinstance(other, Number):
            try:
                result = self.value + other.value
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

        from gladlang.values.primitives.string import String

        if isinstance(other, String):
            return (
                String(int_to_str(self.value) + other.value).set_context(self.context),
                None,
            )

        return None, self._illegal(other)
