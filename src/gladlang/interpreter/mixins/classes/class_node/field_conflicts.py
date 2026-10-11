"""Check that no static field has the same name as an inherited method."""

from gladlang.core.errors import RuntimeError


class InterpreterClassNodeFieldConflicts:
    def _check_static_fields_vs_methods(
        self,
        result,
        class_node,
        context,
        class_name,
        class_value,
        static_table,
        methods,
    ):
        for field_name in static_table.symbols:
            if field_name in methods:
                continue

            for ancestor in class_value.mro:
                if ancestor is class_value:
                    continue

                if field_name in ancestor.methods:
                    return result.failure(
                        RuntimeError(
                            class_node.position_start,
                            class_node.position_end,
                            f"'{field_name}' is already defined as a method "
                            f"(inherited from '{ancestor.name}') and cannot "
                            f"also be a static field in class '{class_name}'",
                            context,
                        )
                    )

        return None
