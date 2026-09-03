"""Visitor for binary operators: AND/OR, IS, INSTANCEOF, and arithmetic."""

from gladlang.core.constants import GL_KEYWORD
from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number


class InterpreterBinaryOperator:
    def visit_BinaryOperatorNode(self, node, context):
        result = RuntimeResult()

        left_value = result.register(self.visit(node.left_node, context))
        if result.error:
            return result

        if node.operator_token.matches(GL_KEYWORD, "AND"):
            if not left_value.is_true():
                return result.success(
                    Number.false.copy()
                    .set_position(node.position_start, node.position_end)
                    .set_context(context)
                )

            right_value = result.register(self.visit(node.right_node, context))
            if result.error:
                return result

            and_result, error = left_value.anded_by(right_value)
            if error:
                return result.failure(error)

            normalized = (Number.true if and_result.is_true() else Number.false).copy()
            return result.success(
                normalized.set_position(
                    node.position_start, node.position_end
                ).set_context(context)
            )

        elif node.operator_token.matches(GL_KEYWORD, "OR"):
            if left_value.is_true():
                return result.success(
                    Number.true.copy()
                    .set_position(node.position_start, node.position_end)
                    .set_context(context)
                )

            right_value = result.register(self.visit(node.right_node, context))
            if result.error:
                return result

            or_result, error = left_value.ored_by(right_value)
            if error:
                return result.failure(error)

            normalized = (Number.true if or_result.is_true() else Number.false).copy()
            return result.success(
                normalized.set_position(
                    node.position_start, node.position_end
                ).set_context(context)
            )

        right_value = result.register(self.visit(node.right_node, context))
        if result.error:
            return result

        if node.operator_token.matches(GL_KEYWORD, "IS"):
            comparison_result, error = left_value.get_comparison_is(right_value)
            if error:
                return result.failure(error)

            return result.success(
                comparison_result.set_position(node.position_start, node.position_end)
            )

        elif node.operator_token.matches(GL_KEYWORD, "INSTANCEOF"):
            comparison_result, error = left_value.get_comparison_instanceof(right_value)
            if error:
                return result.failure(error)

            return result.success(
                comparison_result.set_position(node.position_start, node.position_end)
            )

        operation = self._binary_operator_dispatch.get(node.operator_token.type)
        if operation is None:
            return result.failure(
                RuntimeError(
                    node.operator_token.position_start,
                    node.operator_token.position_end,
                    f"Unsupported operator '{node.operator_token.type}'",
                    context,
                )
            )

        operator_result, error = operation(left_value, right_value)
        if error:
            error.position_start = node.position_start
            error.position_end = node.position_end
            error.context = context

            return result.failure(error)

        return result.success(
            operator_result.set_position(node.position_start, node.position_end)
        )
