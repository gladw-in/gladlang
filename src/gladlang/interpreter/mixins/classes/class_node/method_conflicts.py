"""Check that no method has the same name as a static field (own or inherited)."""

from gladlang.core.errors import RuntimeError


class InterpreterClassNodeMethodConflicts:
    def _check_methods_vs_static_fields(
        self,
        result,
        class_node,
        context,
        class_name,
        class_value,
        static_table,
        methods,
    ):
        for method_name in methods:
            if method_name in static_table.symbols:
                return result.failure(
                    RuntimeError(
                        class_node.position_start,
                        class_node.position_end,
                        f"'{method_name}' is already defined as a static "
                        f"field in class '{class_name}' and cannot also "
                        "be a method",
                        context,
                    )
                )

            for ancestor in class_value.mro:
                if ancestor is class_value:
                    continue

                if method_name in ancestor.static_symbol_table.symbols:
                    return result.failure(
                        RuntimeError(
                            class_node.position_start,
                            class_node.position_end,
                            f"'{method_name}' is already defined as a static "
                            f"field (inherited from '{ancestor.name}') and cannot "
                            f"also be a method in class '{class_name}'",
                            context,
                        )
                    )

        return None
