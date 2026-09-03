"""Number bit-shift operations: <<, >>."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings


class NumberShifts:
    __slots__ = ()

    def lshifted_by(self, other):
        if hasattr(other, "_is_null") and other._is_null:
            return None, self._illegal(other)

        from gladlang.values.primitives.number import Number

        if isinstance(other, Number):
            shift_amount = int(other.value)
            if shift_amount < 0:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Negative shift count",
                    self.context,
                )

            if shift_amount >= Settings.BITWISE_MAX_SHIFT:
                return Number(0).set_context(self.context), None

            raw = (int(self.value) << shift_amount) & Settings.BITWISE_MASK
            if raw & Settings.BITWISE_SIGN_BIT:
                raw -= Settings.BITWISE_COMPLEMENT

            return Number(raw).set_context(self.context), None

        return None, self._illegal(other)

    def rshifted_by(self, other):
        if hasattr(other, "_is_null") and other._is_null:
            return None, self._illegal(other)

        from gladlang.values.primitives.number import Number

        if isinstance(other, Number):
            shift_amount = int(other.value)
            if shift_amount < 0:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "Negative shift count",
                    self.context,
                )

            if shift_amount >= Settings.BITWISE_MAX_SHIFT:
                return (Number(-1) if int(self.value) < 0 else Number(0)).set_context(
                    self.context
                ), None

            raw = int(self.value) >> shift_amount
            masked = raw & Settings.BITWISE_MASK
            result = (
                masked - Settings.BITWISE_COMPLEMENT
                if masked & Settings.BITWISE_SIGN_BIT
                else masked
            )

            return Number(result).set_context(self.context), None

        return None, self._illegal(other)
