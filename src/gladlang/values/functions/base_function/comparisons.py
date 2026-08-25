"""BaseFunction comparisons (==, !=, IS) and logical operators (AND, OR)."""

from gladlang.values.primitives.number import Number


class BaseFunctionComparisons:
    __slots__ = ()

    def get_comparison_eq(self, other, visited=None):
        if hasattr(other, "_is_null"):
            return Number(0).set_context(self.context), None

        from gladlang.values.functions.base_function import BaseFunction

        if isinstance(other, BaseFunction):
            return Number(1 if self is other else 0).set_context(self.context), None

        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        if hasattr(other, "_is_null"):
            return Number(1).set_context(self.context), None

        from gladlang.values.functions.base_function import BaseFunction

        if isinstance(other, BaseFunction):
            return Number(1 if self is not other else 0).set_context(self.context), None

        return None, self.illegal_operation(other)

    def get_comparison_is(self, other):
        return Number(1 if self is other else 0).set_context(self.context), None

    def anded_by(self, other):
        is_true = self.is_true() and other.is_true()
        return Number(1 if is_true else 0).set_context(self.context), None

    def ored_by(self, other):
        is_true = self.is_true() or other.is_true()
        return Number(1 if is_true else 0).set_context(self.context), None
