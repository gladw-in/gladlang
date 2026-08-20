"""Finish parsing a plain list literal with comma-separated elements."""

from gladlang.core.constants import GL_COMMA, GL_RSQUARE
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import ListNode


class ParserListPlain:
    def _finish_plain_list(self, result, first_expression, start_position):
        elements = [first_expression]

        while self.current_token.type == GL_COMMA:
            result.register_advancement()
            self.advance()

            if self.current_token.type == GL_RSQUARE:
                break

            elements.append(result.register(self.expression()))
            if result.error:
                return result

        if self.current_token.type != GL_RSQUARE:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected ',' or ']'",
                )
            )

        result.register_advancement()
        self.advance()

        return result.success(
            ListNode(elements, start_position, self.current_token.position_start.copy())
        )
