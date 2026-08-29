"""Visitor for PUBLIC/PRIVATE/PROTECTED/FINAL-qualified assignment statements."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.parser.ast import SetAttributeNode, VariableAssignNode


class InterpreterVisibilityStatement:
    def visit_VisibilityStatementNode(self, node, context):
        result = RuntimeResult()

        target_visibility = getattr(node, "target_visibility", node.visibility)
        if target_visibility == "FINAL":
            target_visibility = "PUBLIC"

        is_final = getattr(node, "is_final", False)

        if isinstance(node.assign_node, SetAttributeNode):
            instance = result.register(
                self.visit(node.assign_node.object_node, context)
            )

            if result.error:
                return result

            value = result.register(self.visit(node.assign_node.value_node, context))
            if result.error:
                return result

            _, error = instance.set_attribute(
                node.assign_node.attribute_name_token,
                value,
                context,
                visibility=target_visibility,
                as_final=is_final,
            )

            if error:
                return result.failure(error)

            return result.success(value)

        elif isinstance(node.assign_node, VariableAssignNode):
            variable_name = node.assign_node.variable_name_token.value
            value = result.register(self.visit(node.assign_node.value_node, context))
            if result.error:
                return result

            if is_final:
                error = context.symbol_table.set_if_absent(
                    variable_name, value, visibility=target_visibility, as_final=True
                )

                if error:
                    return result.failure(
                        RuntimeError(
                            node.position_start, node.position_end, error, context
                        )
                    )

                return result.success(value)

            context.symbol_table.set(variable_name, value, visibility=target_visibility)

            return result.success(value)

        return result.failure(
            RuntimeError(
                node.position_start,
                node.position_end,
                "Invalid visibility statement",
                context,
            )
        )
