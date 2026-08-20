"""Visitors for single-variable assignment: LET/plain assignment and FINAL declarations."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult


class InterpreterVariableAssign:
    def visit_VariableAssignNode(self, node, context):
        result = RuntimeResult()

        if context is None:
            return result.failure(
                RuntimeError(
                    node.position_start,
                    node.position_end,
                    "Internal error: missing execution context",
                    None,
                )
            )

        variable_name = node.variable_name_token.value
        value = result.register(self.visit(node.value_node, context))
        if result.error:
            return result

        visibility = getattr(node, "target_visibility", "PUBLIC")

        if node.is_declaration:
            error = context.symbol_table.set_if_absent(
                variable_name, value, visibility=visibility
            )

            if error:
                return result.failure(
                    RuntimeError(node.position_start, node.position_end, error, context)
                )
        else:
            error = context.symbol_table.update(variable_name, value)
            if error:
                return result.failure(
                    RuntimeError(node.position_start, node.position_end, error, context)
                )

        return result.success(value)

    def visit_FinalVariableAssignNode(self, node, context):
        result = RuntimeResult()

        variable_name = node.variable_name_token.value
        value = result.register(self.visit(node.value_node, context))
        if result.error:
            return result

        error = context.symbol_table.set_if_absent(variable_name, value, as_final=True)
        if error:
            return result.failure(
                RuntimeError(node.position_start, node.position_end, error, context)
            )

        return result.success(value)
