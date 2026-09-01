"""List comparisons (==, !=, IS) and logical operators (AND, OR, NOT)."""

from gladlang.values.nulls.frozen_null import FrozenNull
from gladlang.values.nulls.mutable_null import MutableNull
from gladlang.values.primitives.number import Number


class ListComparisons:
    __slots__ = ()

    def get_comparison_eq(self, other, visited=None):
        from gladlang.values.primitives.list import List

        if isinstance(other, (FrozenNull, MutableNull)):
            return (Number(0).set_context(self.context), None)

        if not isinstance(other, List):
            return (None, self._illegal(other))

        if len(self.elements) != len(other.elements):
            return (Number(0).set_context(self.context), None)

        if visited is None:
            visited = set()

        visited_pair = (id(self), id(other))
        if visited_pair in visited:
            return (Number(1).set_context(self.context), None)

        visited.add(visited_pair)

        try:
            for index in range(len(self.elements)):
                result, error = self.elements[index].get_comparison_eq(
                    other.elements[index], visited
                )

                if error:
                    return (None, error)

                if not result.is_true():
                    return (Number(0).set_context(self.context), None)

        finally:
            visited.remove(visited_pair)

        return (Number(1).set_context(self.context), None)

    def get_comparison_ne(self, other):
        from gladlang.values.primitives.list import List

        if isinstance(other, (FrozenNull, MutableNull)):
            return Number(1).set_context(self.context), None

        if not isinstance(other, List):
            return None, self._illegal(other)

        result, error = self.get_comparison_eq(other)
        if error:
            return None, error

        return (Number(0) if result.is_true() else Number(1)).set_context(
            self.context
        ), None

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

    def notted(self):
        return Number(0 if self.is_true() else 1).set_context(self.context), None
