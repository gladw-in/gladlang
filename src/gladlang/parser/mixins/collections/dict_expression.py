"""Parse a dict literal or comprehension, starting with { and key:value."""

from gladlang.core.constants import GL_COLON, GL_KEYWORD, GL_LBRACE, GL_RBRACE
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import DictNode
from gladlang.parser.parse_result import ParseResult


class ParserDictExpression:
    def dict_expression(self):
        result = ParseResult()
        start_position = self.current_token.position_start.copy()

        if self.current_token.type != GL_LBRACE:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected '{'",
                )
            )

        result.register_advancement()
        self.advance()

        if self.current_token.type == GL_RBRACE:
            result.register_advancement()
            self.advance()
            return result.success(
                DictNode([], start_position, self.current_token.position_start.copy())
            )

        key = result.register(self.expression())
        if result.error:
            return result

        if self.current_token.type != GL_COLON:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected ':'",
                )
            )

        result.register_advancement()
        self.advance()

        value = result.register(self.expression())
        if result.error:
            return result

        if self.current_token.matches(GL_KEYWORD, "FOR"):
            return self._finish_dict_comprehension(result, key, value, start_position)

        return self._finish_plain_dict(result, key, value, start_position)
