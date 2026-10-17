"""Bitwise OR (|) for numbers."""

from gladlang.core.util.numbers import require_integer_number
from gladlang.core.util.settings import Settings


class NumberBitwiseOr:
    __slots__ = ()

    def bitted_or_by(self, other):
        if hasattr(other, "_is_null") and other._is_null:
            return None, self._illegal(other)

        from gladlang.values.primitives.number import Number

        if isinstance(other, Number):
            left, error = require_integer_number(
                self.value,
                self.position_start,
                self.position_end,
                self.context,
                "Left operand",
            )

            if error:
                return None, error

            right, error = require_integer_number(
                other.value,
                other.position_start,
                other.position_end,
                self.context,
                "Right operand",
            )

            if error:
                return None, error

            raw_value = (left | right) & Settings.BITWISE_MASK
            if raw_value & Settings.BITWISE_SIGN_BIT:
                raw_value -= Settings.BITWISE_COMPLEMENT

            return Number(raw_value).set_context(self.context), None

        return None, self._illegal(other)
