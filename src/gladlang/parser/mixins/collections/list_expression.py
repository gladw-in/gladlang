"""Parse a list literal or comprehension."""

from gladlang.core.constants import GL_KEYWORD, GL_LSQUARE, GL_RSQUARE
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import ListNode
from gladlang.parser.parse_result import ParseResult


class ParserListExpression:
    def list_expression(self):
        result = ParseResult()
        start_position = self.current_token.position_start.copy()

        if self.current_token.type != GL_LSQUARE:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected '['",
                )
            )

        result.register_advancement()
        self.advance()

        if self.current_token.type == GL_RSQUARE:
            result.register_advancement()
            self.advance()

            return result.success(
                ListNode([], start_position, self.current_token.position_start.copy())
            )

        first_expression = result.register(self.expression())
        if result.error:
            return result

        if self.current_token.matches(GL_KEYWORD, "FOR"):
            return self._finish_list_comprehension(
                result, first_expression, start_position
            )

        return self._finish_plain_list(result, first_expression, start_position)
