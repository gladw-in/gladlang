"""Reading a variable's value or visibility, walking up through parent scopes."""


class SymbolTableGetOperators:
    def get(self, name):
        scope = self
        while scope is not None:
            if name in scope.finals:
                with scope._lock:
                    value = scope.symbols.get(name)
                    if value is not None:
                        return value

            with scope._lock:
                value = scope.symbols.get(name)
                if value is not None:
                    return value

                parent = scope.parent

            scope = parent

        return None

    def get_visibility(self, name):
        scope = self
        while scope is not None:
            with scope._lock:
                visibility = scope.visibilities.get(name)
                if visibility is not None:
                    return visibility

                parent = scope.parent

            scope = parent

        return "PUBLIC"
