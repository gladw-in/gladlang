"""Boolean and comparison expression parsing (OR, AND, NOT, ==, !=, <, >, IS, INSTANCEOF)."""

from gladlang.core.constants import (
    GL_EE,
    GL_GT,
    GL_GTE,
    GL_KEYWORD,
    GL_LT,
    GL_LTE,
    GL_NE,
)
from gladlang.parser.ast import (
    BinaryOperatorNode,
    ChainedComparisonNode,
    UnaryOperatorNode,
)
from gladlang.parser.parse_result import ParseResult


class ExpressionsBoolean:
    def or_expression(self):
        return self.binary_operator(self.and_expression, ((GL_KEYWORD, "OR"),))

    def and_expression(self):
        return self.binary_operator(self.comparison_expression, ((GL_KEYWORD, "AND"),))

    def logic_expression(self):
        return self.or_expression()

    def comparison_expression(self):
        result = ParseResult()
        if self.current_token.matches(GL_KEYWORD, "NOT"):
            operator_token = self.current_token
            result.register_advancement()
            self.advance()
            node = result.register(self.comparison_expression())
            if result.error:
                return result

            return result.success(UnaryOperatorNode(operator_token, node))

        left_node = result.register(self.bitwise_or_expression())
        if result.error:
            return result

        comparisons = []
        while self.current_token.type in (
            GL_EE,
            GL_NE,
            GL_LT,
            GL_GT,
            GL_LTE,
            GL_GTE,
        ) or (
            self.current_token.type == GL_KEYWORD
            and self.current_token.value in ("IS", "INSTANCEOF")
        ):
            operator_token = self.current_token
            result.register_advancement()
            self.advance()
            right_node = result.register(self.bitwise_or_expression())
            if result.error:
                return result

            comparisons.append((operator_token, right_node))

        if not comparisons:
            return result.success(left_node)

        if len(comparisons) == 1:
            operator_token, right_node = comparisons[0]
            return result.success(
                BinaryOperatorNode(left_node, operator_token, right_node)
            )

        return result.success(ChainedComparisonNode(left_node, comparisons))
