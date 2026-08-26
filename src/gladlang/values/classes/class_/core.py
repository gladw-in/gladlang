"""Class core: slots, construction, MRO, and method overrides."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.runtime.symbol_table import SymbolTable
from gladlang.values.functions.base_function import BaseFunction


class ClassCore(BaseFunction):
    __slots__ = (
        "superclasses",
        "methods",
        "static_symbol_table",
        "mro",
        "_method_cache",
    )

    def __init__(self, name, superclasses, methods, static_symbol_table=None, mro=None):
        super().__init__(name)
        self.superclasses = superclasses
        self.methods = methods
        self.static_symbol_table = (
            static_symbol_table if static_symbol_table else SymbolTable()
        )
        self.mro = mro if mro else [self]
        self._method_cache = {}

    def execute(self, arguments, interpreter=None, calling_context=None):
        return RuntimeResult().failure(
            RuntimeError(
                self.position_start,
                self.position_end,
                f"Class '{self.name}' must be instantiated using 'NEW'",
                self.context,
            )
        )

    def copy(self):
        from gladlang.values.classes.class_ import Class

        class_copy = Class(
            self.name,
            self.superclasses[:],
            self.methods,
            self.static_symbol_table.copy(),
            self.mro[:],
        )

        class_copy._method_cache = self._method_cache
        class_copy.set_context(self.context)
        class_copy.set_position(self.position_start, self.position_end)

        return class_copy

    def __repr__(self):
        return f"<class {self.name}>"
