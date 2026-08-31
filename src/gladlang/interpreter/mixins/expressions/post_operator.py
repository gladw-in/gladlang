"""Visitor for postfix increment/decrement, returning the old value."""

from gladlang.core.constants import GL_PLUSPLUS
from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number
from gladlang.parser.ast import GetAttributeNode, ListAccessNode, VariableAccessNode


class InterpreterPostOperator:
    def visit_PostOperatorNode(self, node, context):
        result = RuntimeResult()

        target = node.node
        if isinstance(target, VariableAccessNode):
            variable_name = target.variable_name_token.value
            old_value = context.symbol_table.get(variable_name)
            if old_value is None:
                return result.failure(
                    RuntimeError(
                        target.position_start,
                        target.position_end,
                        f"'{variable_name}' is not defined",
                        context,
                    )
                )

        elif isinstance(target, GetAttributeNode):
            instance = result.register(self.visit(target.object_node, context))
            if result.error:
                return result

            old_value, error = instance.get_attribute(
                target.attribute_name_token, context
            )

            if error:
                return result.failure(error)

        elif isinstance(target, ListAccessNode):
            list_value = result.register(self.visit(target.list_node, context))
            if result.error:
                return result

            index_value = result.register(self.visit(target.index_node, context))
            if result.error:
                return result

            old_value, error = list_value.get_element_at(index_value)
            if error:
                return result.failure(error)

        else:
            return result.failure(
                RuntimeError(
                    target.position_start,
                    target.position_end,
                    "Invalid target for increment/decrement",
                    context,
                )
            )

        if not isinstance(old_value, Number) or hasattr(old_value, "_is_null"):
            return result.failure(
                RuntimeError(
                    target.position_start,
                    target.position_end,
                    "Operand must be a number",
                    context,
                )
            )

        if node.operator_token.type == GL_PLUSPLUS:
            new_value, error = old_value.added_to(Number(1))
        else:
            new_value, error = old_value.subbed_by(Number(1))

        if error:
            return result.failure(error)

        if isinstance(target, VariableAccessNode):
            update_error = context.symbol_table.update(variable_name, new_value)
            if update_error:
                return result.failure(
                    RuntimeError(
                        target.position_start,
                        target.position_end,
                        update_error,
                        context,
                    )
                )

        elif isinstance(target, GetAttributeNode):
            _, error = instance.set_attribute(
                target.attribute_name_token, new_value, context
            )

            if error:
                return result.failure(error)

        elif isinstance(target, ListAccessNode):
            _, error = list_value.set_element_at(index_value, new_value)
            if error:
                return result.failure(error)

        return result.success(
            old_value.copy().set_position(node.position_start, node.position_end)
        )
