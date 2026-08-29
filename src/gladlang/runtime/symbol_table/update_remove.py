"""Reassign existing variables (walking scopes) and remove from current scope."""


class SymbolTableUpdateRemove:
    def update(self, name, value):
        scope = self
        while scope is not None:
            with scope._lock:
                if name in scope.finals:
                    return f"Cannot reassign constant '{name}'"

                if name in scope.symbols:
                    scope.symbols[name] = value
                    return None

                parent = scope.parent

            scope = parent

        return f"'{name}' is not defined"

    def remove(self, name):
        with self._lock:
            self.symbols.pop(name, None)
            if name in self.finals:
                self.finals.discard(name)
                self._finals_count = max(0, self._finals_count - 1)

            self.visibilities.pop(name, None)
            self.defining_classes.pop(name, None)
