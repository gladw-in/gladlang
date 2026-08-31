"""String comparisons (==, !=, <, >, <=, >=, IS) and logical operators (AND, OR, NOT)."""

from gladlang.values.nulls.frozen_null import FrozenNull
from gladlang.values.nulls.mutable_null import MutableNull
from gladlang.values.primitives.number import Number


class StringComparisons:
    __slots__ = ()

    def get_comparison_eq(self, other, visited=None):
        from gladlang.values.primitives.string import String

        if isinstance(other, (FrozenNull, MutableNull)):
            return Number(0).set_context(self.context), None

        if isinstance(other, String):
            return (
                Number(int(self.value == other.value)).set_context(self.context),
                None,
            )

        return None, self._illegal(other)

    def get_comparison_ne(self, other):
        from gladlang.values.primitives.string import String

        if isinstance(other, (FrozenNull, MutableNull)):
            return Number(1).set_context(self.context), None

        if isinstance(other, String):
            return (
                Number(int(self.value != other.value)).set_context(self.context),
                None,
            )

        return None, self._illegal(other)

    def get_comparison_lt(self, other):
        from gladlang.values.primitives.string import String

        if isinstance(other, String):
            return Number(int(self.value < other.value)).set_context(self.context), None

        return None, self._illegal(other)

    def get_comparison_gt(self, other):
        from gladlang.values.primitives.string import String

        if isinstance(other, String):
            return Number(int(self.value > other.value)).set_context(self.context), None

        return None, self._illegal(other)

    def get_comparison_lte(self, other):
        from gladlang.values.primitives.string import String

        if isinstance(other, String):
            return (
                Number(int(self.value <= other.value)).set_context(self.context),
                None,
            )

        return None, self._illegal(other)

    def get_comparison_gte(self, other):
        from gladlang.values.primitives.string import String

        if isinstance(other, String):
            return (
                Number(int(self.value >= other.value)).set_context(self.context),
                None,
            )

        return None, self._illegal(other)

    def get_comparison_is(self, other):
        return Number(1 if self is other else 0).set_context(self.context), None

    def anded_by(self, other):
        is_true = self.is_true() and other.is_true()
        return Number(1 if is_true else 0).set_context(self.context), None

    def ored_by(self, other):
        is_true = self.is_true() or other.is_true()
        return Number(1 if is_true else 0).set_context(self.context), None

    def notted(self):
        return Number(0 if self.is_true() else 1).set_context(self.context), None
