"""Number right bit-shift operation."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.numbers import require_integer_number
from gladlang.core.util.settings import Settings


class NumberShiftsRightShift:
    __slots__ = ()

    def right_shifted_by(self, other):
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
                return (Number(-1) if left < 0 else Number(0)).set_context(
                    self.context
                ), None

            raw_value = left >> shift_amount
            masked = raw_value & Settings.BITWISE_MASK
            result = (
                masked - Settings.BITWISE_COMPLEMENT
                if masked & Settings.BITWISE_SIGN_BIT
                else masked
            )

            return Number(result).set_context(self.context), None

        return None, self._illegal(other)
