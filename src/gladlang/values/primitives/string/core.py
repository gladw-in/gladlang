"""Core String with slots and protocol methods."""

from gladlang.core.errors import RuntimeError
from gladlang.values.value import Value


class StringCore(Value):
    __slots__ = ("value", "position_start", "position_end", "context")

    def __init__(self, value):
        self.value = value
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
        return len(self.value) > 0

    def copy(self):
        from gladlang.values.primitives.string import String

        string_copy = String(self.value)
        string_copy.set_position(self.position_start, self.position_end)
        string_copy.set_context(self.context)
        return string_copy

    def execute(self, arguments, interpreter=None, calling_context=None):
        from gladlang.runtime.runtime_result import RuntimeResult

        return RuntimeResult().failure(self._illegal())

    def get_attribute(self, name_token, context=None):
        return None, self._illegal()

    def set_attribute(
        self, name_token, value, context=None, visibility=None, as_final=False
    ):
        return None, self._illegal()

    def set_element_at(self, index, value):
        return None, self._illegal()

    def _illegal(self, other=None):
        if not other:
            other = self

        return RuntimeError(
            self.position_start, other.position_end, "Illegal operation", self.context
        )

    def illegal_operation(self, other=None):
        return self._illegal(other)

    def __repr__(self):
        return self.value
