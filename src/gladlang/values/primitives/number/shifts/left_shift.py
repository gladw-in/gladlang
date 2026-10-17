"""Number left bit-shift operation."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.numbers import require_integer_number
from gladlang.core.util.settings import Settings


class NumberShiftsLeftShift:
    __slots__ = ()

    def left_shifted_by(self, other):
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

            shift_amount, error = require_integer_number(
                other.value,
                other.position_start,
                other.position_end,
                self.context,
                "Shift amount",
            )

            if error:
                return None, error

            if shift_amount < 0:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Negative shift count",
                    self.context,
                )

            if shift_amount >= Settings.BITWISE_MAX_SHIFT:
                return Number(0).set_context(self.context), None

            raw_value = (left << shift_amount) & Settings.BITWISE_MASK
            if raw_value & Settings.BITWISE_SIGN_BIT:
                raw_value -= Settings.BITWISE_COMPLEMENT

            return Number(raw_value).set_context(self.context), None

        return None, self._illegal(other)
