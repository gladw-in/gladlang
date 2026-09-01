"""Core Super machinery with slots, construction, and method overrides."""

from gladlang.core.errors import RuntimeError
from gladlang.values.primitives.number import Number
from gladlang.values.value import Value


class SuperCore(Value):
    __slots__ = ("instance", "start_class", "position_start", "position_end", "context")

    def __init__(self, instance, start_class):
        self.instance = instance
        self.start_class = start_class
        self.position_start = None
        self.position_end = None
        self.context = None

    def set_position(self, position_start=None, position_end=None):
        self.position_start = position_start
        self.position_end = position_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def is_true(self):
        return True

    def copy(self):
        from gladlang.values.classes.super_ import Super

        super_copy = (
            Super(self.instance, self.start_class)
            .set_context(self.context)
            .set_position(self.position_start, self.position_end)
        )

        return super_copy

    def get_comparison_is(self, other):
        return Number(1 if self is other else 0).set_context(self.context), None

    def _illegal(self, other=None):
        if not other:
            other = self

        return RuntimeError(
            self.position_start, other.position_end, "Illegal operation", self.context
        )

    def illegal_operation(self, other=None):
        return self._illegal(other)
