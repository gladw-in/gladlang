"""Core Enum machinery with slots, construction, and method overrides."""

from gladlang.core.errors import RuntimeError
from gladlang.values.value import Value


class EnumCore(Value):
    __slots__ = (
        "name",
        "elements_dictionary",
        "position_start",
        "position_end",
        "context",
    )

    def __init__(self, name, elements_dictionary):
        self.name = name
        self.elements_dictionary = elements_dictionary
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

    def execute(self, arguments, interpreter=None, calling_context=None):
        from gladlang.runtime.runtime_result import RuntimeResult

        return RuntimeResult().failure(self._illegal())

    def notted(self):
        return None, self._illegal()

    def copy(self):
        from gladlang.values.enums.enum import Enum

        enum_copy = Enum(self.name, self.elements_dictionary)
        enum_copy.set_position(self.position_start, self.position_end)
        enum_copy.set_context(self.context)
        return enum_copy

    def _illegal(self, other=None):
        if not other:
            other = self

        return RuntimeError(
            self.position_start, other.position_end, "Illegal operation", self.context
        )

    def illegal_operation(self, other=None):
        return self._illegal(other)

    def __repr__(self):
        return f"<enum {self.name}>"
