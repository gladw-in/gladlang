"""Boolean AND/OR for Type, based purely on truthiness."""

from gladlang.values.primitives.number import Number


class TypeLogicOperators:
    __slots__ = ()

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
