"""Boolean negation for FunctionGroup values."""

from gladlang.values.primitives.number import Number


class FunctionGroupNotted:
    __slots__ = ()

    def notted(self):
        return Number(0 if self.is_true() else 1).set_context(self.context), None
