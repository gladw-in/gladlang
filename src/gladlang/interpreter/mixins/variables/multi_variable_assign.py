"""Visitor for list-destructuring assignment: LET [a, b, c] = list_expression."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.list import List


class InterpreterMultiVariableAssign:
    def visit_MultiVariableAssignNode(self, node, context):
        result = RuntimeResult()

        list_value = result.register(self.visit(node.value_node, context))
        if result.error:
            return result

        if not isinstance(list_value, List):
            return result.failure(
                RuntimeError(
                    node.position_start,
                    node.position_end,
                    f"Cannot unpack type '{type(list_value).__name__}' (expected List)",
                    context,
                )
            )

        if len(node.var_name_tokens) != len(list_value.elements):
            return result.failure(
                RuntimeError(
                    node.position_start,
                    node.position_end,
                    f"Cannot unpack {len(list_value.elements)} value(s) into {len(node.var_name_tokens)} variable(s)",
                    context,
                )
            )

        for index, variable_token in enumerate(node.var_name_tokens):
            variable_name = variable_token.value

            if node.is_declaration:
                error = context.symbol_table.set_if_absent(
                    variable_name, list_value.elements[index]
                )

                if error:
                    return result.failure(
                        RuntimeError(
                            variable_token.position_start,
                            variable_token.position_end,
                            error,
                            context,
                        )
                    )
            else:
                error = context.symbol_table.update(
                    variable_name, list_value.elements[index]
                )

                if error:
                    return result.failure(
                        RuntimeError(
                            variable_token.position_start,
                            variable_token.position_end,
                            error,
                            context,
                        )
                    )

        return result.success(list_value)
