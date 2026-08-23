"""Type comparisons: IS identity, EQ equality, and the INSTANCEOF operand-type error."""

from gladlang.core.errors import RuntimeError
from gladlang.values.primitives.number import Number


class TypeComparisons:
    __slots__ = ()

    def get_comparison_is(self, other):
        return Number(1 if self is other else 0).set_context(self.context), None

    def get_comparison_eq(self, other, visited=None):
        from gladlang.values.classes.type_ import Type

        if isinstance(other, Type):
            return Number(1 if self is other else 0).set_context(self.context), None

        return None, self._illegal(other)

    def get_comparison_instanceof(self, other):
        return None, RuntimeError(
            self.position_start,
            self.position_end,
            "Right operand of INSTANCEOF must be a Class or Type",
            self.context,
        )
