"""Derive != from ==, and IS is identity comparison."""


class ValueComparisonDerived:
    __slots__ = ()

    def get_comparison_ne(self, other):
        from gladlang.values.primitives.number import Number

        result, error = self.get_comparison_eq(other)
        if error:
            return None, error

        if result.is_true():
            return Number(0).set_context(self.context), None
        else:
            return Number(1).set_context(self.context), None

    def get_comparison_is(self, other):
        from gladlang.values.primitives.number import Number

        return Number(1 if self is other else 0).set_context(self.context), None
