"""Build a new call context for a function invocation."""

from gladlang.runtime.context import Context
from gladlang.runtime.symbol_table import SymbolTable


class BaseFunctionGenerateContext:
    __slots__ = ()

    def generate_new_context(self, calling_context=None):
        parent = calling_context if calling_context is not None else self.context

        new_context = Context(self.name, parent, self.position_start)

        if self.context is None:
            new_context.symbol_table = SymbolTable()
        else:
            new_context.symbol_table = SymbolTable(self.context.symbol_table)

        return new_context
