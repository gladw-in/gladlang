"""Logical AND, OR and NOT for numbers."""


class NumberBitwiseLogical:
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
