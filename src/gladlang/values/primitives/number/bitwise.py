"""Number logical (AND/OR/NOT) and bitwise (&, |, ^, ~) operations. Shifts (<<, >>) live in shifts.py."""

from gladlang.core.util.settings import Settings


class NumberBitwise:
    __slots__ = ()

    def anded_by(self, other):
        from gladlang.values.primitives.number import Number

        if hasattr(other, "is_true"):
            return Number(1 if (self.is_true() and other.is_true()) else 0), None

        return None, self._illegal(other)

    def ored_by(self, other):
        from gladlang.values.primitives.number import Number

        if hasattr(other, "is_true"):
            return Number(1 if (self.is_true() or other.is_true()) else 0), None

        return None, self._illegal(other)

    def notted(self):
        from gladlang.values.primitives.number import Number

        return (Number(0), None) if self.is_true() else (Number(1), None)

    def bitted_and_by(self, other):
        if hasattr(other, "_is_null") and other._is_null:
            return None, self._illegal(other)

        from gladlang.values.primitives.number import Number

        if isinstance(other, Number):
            raw = (int(self.value) & int(other.value)) & Settings.BITWISE_MASK
            if raw & Settings.BITWISE_SIGN_BIT:
                raw -= Settings.BITWISE_COMPLEMENT

            return Number(raw).set_context(self.context), None

        return None, self._illegal(other)

    def bitted_or_by(self, other):
        if hasattr(other, "_is_null") and other._is_null:
            return None, self._illegal(other)

        from gladlang.values.primitives.number import Number

        if isinstance(other, Number):
            raw = (int(self.value) | int(other.value)) & Settings.BITWISE_MASK
            if raw & Settings.BITWISE_SIGN_BIT:
                raw -= Settings.BITWISE_COMPLEMENT

            return Number(raw).set_context(self.context), None

        return None, self._illegal(other)

    def bitted_xor_by(self, other):
        if hasattr(other, "_is_null") and other._is_null:
            return None, self._illegal(other)

        from gladlang.values.primitives.number import Number

        if isinstance(other, Number):
            raw = (int(self.value) ^ int(other.value)) & Settings.BITWISE_MASK
            if raw & Settings.BITWISE_SIGN_BIT:
                raw -= Settings.BITWISE_COMPLEMENT

            return Number(raw).set_context(self.context), None

        return None, self._illegal(other)

    def bitted_not(self):
        from gladlang.values.primitives.number import Number

        raw = (~int(self.value)) & Settings.BITWISE_MASK
        if raw & Settings.BITWISE_SIGN_BIT:
            raw -= Settings.BITWISE_COMPLEMENT

        return Number(raw).set_context(self.context), None
