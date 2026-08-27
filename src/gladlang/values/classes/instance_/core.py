"""Core Instance machinery: slots, construction, copy, and generic protocol stubs."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.symbol_table import SymbolTable
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number
from gladlang.values.value import Value


class InstanceCore(Value):
    __slots__ = (
        "class_reference",
        "symbol_table",
        "position_start",
        "position_end",
        "context",
    )

    def __init__(self, class_reference):
        self.class_reference = class_reference
        self.symbol_table = SymbolTable()
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
        return RuntimeResult().failure(self._illegal())

    def notted(self):
        return Number(0 if self.is_true() else 1).set_context(self.context), None

    def copy(self):
        from gladlang.values.classes.instance_ import Instance

        instance_copy = Instance(self.class_reference)

        for name, value in self.symbol_table.symbols.items():
            instance_copy.symbol_table.symbols[name] = value
            if name in self.symbol_table.visibilities:
                instance_copy.symbol_table.visibilities[name] = (
                    self.symbol_table.visibilities[name]
                )

            if name in self.symbol_table.finals:
                instance_copy.symbol_table.finals.add(name)

            if name in self.symbol_table.defining_classes:
                instance_copy.symbol_table.defining_classes[name] = (
                    self.symbol_table.defining_classes[name]
                )

        instance_copy.symbol_table._finals_count = len(
            instance_copy.symbol_table.finals
        )

        instance_copy.set_context(self.context)
        instance_copy.set_position(self.position_start, self.position_end)
        return instance_copy

    def _illegal(self, other=None):
        if not other:
            other = self

        return RuntimeError(
            self.position_start, other.position_end, "Illegal operation", self.context
        )

    def illegal_operation(self, other=None):
        return self._illegal(other)

    def __repr__(self):
        return f"<{self.class_reference.name} instance>"
