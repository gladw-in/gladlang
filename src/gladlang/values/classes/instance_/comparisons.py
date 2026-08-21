"""Comparisons, identity, logical operators, and INSTANCEOF."""

from gladlang.core.errors import RuntimeError
from gladlang.values.nulls.frozen_null import FrozenNull
from gladlang.values.nulls.mutable_null import MutableNull
from gladlang.values.primitives.number import Number
from gladlang.values.classes.class_ import Class
from gladlang.values.classes.type_ import Type


class InstanceComparisons:
    def get_comparison_eq(self, other, visited=None):
        if isinstance(other, (FrozenNull, MutableNull)):
            return Number(0).set_context(self.context), None

        if isinstance(other, InstanceComparisons):
            return Number(1 if self is other else 0).set_context(self.context), None

        return None, self._illegal(other)

    def get_comparison_ne(self, other):
        if isinstance(other, (FrozenNull, MutableNull)):
            return Number(1).set_context(self.context), None

        if isinstance(other, InstanceComparisons):
            return Number(1 if self is not other else 0).set_context(self.context), None

        return None, self._illegal(other)

    def get_comparison_is(self, other):
        return Number(1 if self is other else 0).set_context(self.context), None

    def get_comparison_instanceof(self, other):
        if isinstance(other, Class):
            return (
                Number(1 if other in self.class_reference.mro else 0).set_context(
                    self.context
                ),
                None,
            )

        if isinstance(other, Type):
            if other.name == "Object":
                return Number.true.copy(), None
            return Number.false.copy(), None

        return None, RuntimeError(
            self.position_start,
            self.position_end,
            "Right operand of INSTANCEOF must be a Class or Type",
            self.context,
        )

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
