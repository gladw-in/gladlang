"""Number arithmetic: division, modulo, floor division."""

import math

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings


class NumberArithmeticDivMod:
    __slots__ = ()

    def dived_by(self, other):
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

    def modded_by(self, other):
        from gladlang.values.primitives.number import Number

        if isinstance(other, Number):
            if not other.value:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Division by zero",
                    self.context,
                )

            result = self.value % other.value
            if isinstance(result, int) and result.bit_length() > Settings.MAX_INT_BITS:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Arithmetic result too large (exceeds integer size limit)",
                    self.context,
                )

            return Number(result).set_context(self.context), None

        return None, self._illegal(other)

    def floordived_by(self, other):
        from gladlang.values.primitives.number import Number

        if isinstance(other, Number):
            if not other.value:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Division by zero",
                    self.context,
                )

            result = self.value // other.value
            if isinstance(result, int) and result.bit_length() > Settings.MAX_INT_BITS:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Arithmetic result too large (exceeds integer size limit)",
                    self.context,
                )

            return Number(result).set_context(self.context), None

        return None, self._illegal(other)
