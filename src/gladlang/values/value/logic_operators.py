"""Generic AND/OR based purely on truthiness — works for any two Values."""


class ValueLogicOperators:
    __slots__ = ()

    def anded_by(self, other):
        from gladlang.values.primitives.number import Number

        is_true = self.is_true() and other.is_true()

        return Number(1 if is_true else 0).set_context(self.context), None

    def ored_by(self, other):
        from gladlang.values.primitives.number import Number

        is_true = self.is_true() or other.is_true()

        return Number(1 if is_true else 0).set_context(self.context), None
