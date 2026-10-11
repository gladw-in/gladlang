"""Evaluate the static fields of a class inside the class's own scope."""

from gladlang.runtime.context import Context


class InterpreterClassNodeStaticFields:
    def _evaluate_static_fields(
        self, result, class_node, context, class_name, class_value, static_table
    ):
        class_context = Context(
            f"<class {class_name}>", context, class_node.position_start
        )
        class_context.symbol_table = static_table
        class_context.active_class = class_value

        for field_node in class_node.static_field_nodes:
            result.register(self.visit(field_node, class_context))
            if result.error:
                return result

        static_table.parent = None

        return None
