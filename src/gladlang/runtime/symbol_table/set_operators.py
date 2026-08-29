"""Set and declare variables with visibility and constancy."""


class SymbolTableSetOperators:
    def set(
        self, name, value, visibility="PUBLIC", as_final=False, defining_class=None
    ):
        with self._lock:
            self.symbols[name] = value
            if visibility != "PUBLIC":
                self.visibilities[name] = visibility
            else:
                self.visibilities.pop(name, None)

            if as_final:
                if name not in self.finals:
                    self.finals.add(name)
                    self._finals_count += 1

            if defining_class:
                self.defining_classes[name] = defining_class

    def is_final_in_ancestors(self, name):
        scope = self.parent
        while scope:
            if name in scope.finals:
                with scope._lock:
                    if name in scope.finals:
                        return True

            scope = scope.parent
        return False

    def set_if_absent(self, name, value, visibility="PUBLIC", as_final=False):
        with self._lock:
            if name in self.symbols:
                return f"Variable '{name}' is already defined"

            if as_final and self.is_final_in_ancestors(name):
                return f"Cannot declare constant '{name}' because it is already defined as constant in outer scope"

            self.symbols[name] = value
            if visibility != "PUBLIC":
                self.visibilities[name] = visibility

            if as_final:
                self.finals.add(name)
                self._finals_count += 1

            return None
