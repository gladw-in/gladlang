"""Visitor for chained comparisons left-to-right, short-circuit on false."""

from gladlang.core.constants import (
    GL_EE,
    GL_GT,
    GL_GTE,
    GL_KEYWORD,
    GL_LT,
    GL_LTE,
    GL_NE,
)
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number


class InterpreterChainedComparison:
    def visit_ChainedComparisonNode(self, node, context):
        result = RuntimeResult()

        left_value = result.register(self.visit(node.left_node, context))
        if result.error:
            return result

        for operator_token, right_expression in node.operators_and_expressions:
            right_value = result.register(self.visit(right_expression, context))
            if result.error:
                return result

            comparison_result = None
            error = None

            if operator_token.type == GL_EE:
                comparison_result, error = left_value.get_comparison_eq(right_value)
            elif operator_token.type == GL_NE:
                comparison_result, error = left_value.get_comparison_ne(right_value)
            elif operator_token.type == GL_LT:
                comparison_result, error = left_value.get_comparison_lt(right_value)
            elif operator_token.type == GL_GT:
                comparison_result, error = left_value.get_comparison_gt(right_value)
            elif operator_token.type == GL_LTE:
                comparison_result, error = left_value.get_comparison_lte(right_value)
            elif operator_token.type == GL_GTE:
                comparison_result, error = left_value.get_comparison_gte(right_value)
            elif operator_token.matches(GL_KEYWORD, "IS"):
                comparison_result, error = left_value.get_comparison_is(right_value)

            if error:
                return result.failure(error)

            if not comparison_result.is_true():
                return result.success(Number.false.copy())

            left_value = right_value

        return result.success(Number.true.copy())
