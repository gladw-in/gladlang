"""Ternary conditional expression parsing: condition ? true_case : false_case."""

from gladlang.core.constants import GL_COLON, GL_QMARK
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import TernaryOperatorNode
from gladlang.parser.parse_result import ParseResult


class ExpressionsTernary:
    def ternary_expression(self):
        result = ParseResult()
        condition = result.register(self.logic_expression())
        if result.error:
            return result

        if self.current_token.type == GL_QMARK:
            result.register_advancement()
            self.advance()
            true_case = result.register(self.expression())
            if result.error:
                return result

            if self.current_token.type != GL_COLON:
                return result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected ':' in ternary operator",
                    )
                )

            result.register_advancement()
            self.advance()
            false_case = result.register(self.ternary_expression())
            if result.error:
                return result

            return result.success(TernaryOperatorNode(condition, true_case, false_case))

        return result.success(condition)
