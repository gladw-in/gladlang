"""Enum comparisons (==, !=, IS) and logical operators (AND, OR)."""

from gladlang.values.primitives.number import Number


class EnumComparisons:
    __slots__ = ()

    def get_comparison_eq(self, other, visited=None):
        from gladlang.values.enums.enum import Enum

        if isinstance(other, Enum):
            return Number(1 if self is other else 0).set_context(self.context), None

        return None, self._illegal(other)

    def get_comparison_ne(self, other):
        from gladlang.values.enums.enum import Enum

        if isinstance(other, Enum):
            return Number(1 if self is not other else 0).set_context(self.context), None

        return None, self._illegal(other)

    def get_comparison_is(self, other):
        return Number(1 if self is other else 0).set_context(self.context), None

    def anded_by(self, other):
        return (
            Number(1 if (self.is_true() and other.is_true()) else 0).set_context(
                self.context
            ),
            None,
        )

    def ored_by(self, other):
        return (
            Number(1 if (self.is_true() or other.is_true()) else 0).set_context(
                self.context
            ),
            None,
        )
