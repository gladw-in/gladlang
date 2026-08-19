"""BaseFunction core with slots and method overrides."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.value import Value


class BaseFunctionCore(Value):
    __slots__ = ("name", "position_start", "position_end", "context")

    def __init__(self, name):
        self.name = name or "<anonymous>"
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
        raise Exception("Cannot copy a BaseFunction")

    def execute(self, arguments, interpreter, calling_context=None):
        return RuntimeResult().failure(
            RuntimeError(
                self.position_start,
                self.position_end,
                "BaseFunction cannot be executed",
                self.context,
            )
        )

    def illegal_operation(self, other=None):
        if not other:
            other = self

        return RuntimeError(
            self.position_start, other.position_end, "Illegal operation", self.context
        )

    def __repr__(self):
        return f"<function {self.name}>"
