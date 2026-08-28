"""Core SymbolTable machinery: construction and copy."""

from threading import RLock

from gladlang.core.util.locking import NoLock
from gladlang.core.util.settings import Settings


class SymbolTableCore:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
        self.finals = set()
        self.visibilities = {}
        self.defining_classes = {}
        self._lock = RLock() if Settings.THREADING_ENABLED else NoLock()
        self._finals_count = 0

    def copy(self):
        from gladlang.runtime.symbol_table import SymbolTable

        with self._lock:
            new_symbol_table = SymbolTable(self.parent)
            new_symbol_table.symbols = self.symbols.copy()
            new_symbol_table.visibilities = self.visibilities.copy()
            new_symbol_table.finals = self.finals.copy()
            new_symbol_table.defining_classes = self.defining_classes.copy()
            new_symbol_table._finals_count = len(new_symbol_table.finals)

            return new_symbol_table
