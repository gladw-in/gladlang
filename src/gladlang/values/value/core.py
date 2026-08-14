"""Core Value machinery: slots, construction, and identity/copy defaults."""

from gladlang.core.errors import RuntimeError


class ValueCore:
    __slots__ = ("position_start", "position_end", "context")

    def __init__(self):
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
        raise Exception("No copy method defined")

    def illegal_operation(self, other=None):
        if not other:
            other = self

        return RuntimeError(
            self.position_start, other.position_end, "Illegal operation", self.context
        )
