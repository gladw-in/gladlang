"""Check that a class name does not clash with a constant."""

from gladlang.core.errors import RuntimeError


class InterpreterClassNodeValidateName:
    def _validate_class_name(self, result, class_node, context, class_name):
        if class_name in context.symbol_table.finals:
            return result.failure(
                RuntimeError(
                    class_node.position_start,
                    class_node.position_end,
                    f"Cannot override constant '{class_name}' "
                    "with a class definition",
                    context,
                )
            )

        if context.symbol_table.is_final_in_ancestors(class_name):
            return result.failure(
                RuntimeError(
                    class_node.position_start,
                    class_node.position_end,
                    f"Cannot shadow constant '{class_name}' " "with a class definition",
                    context,
                )
            )

        return None
