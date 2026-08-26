"""FOR statement entry point – dispatches to C-style or iterator-style loop parsing."""

from gladlang.core.constants import GL_KEYWORD, GL_LPAREN
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.parse_result import ParseResult


class StatementsForDispatch:
    def for_expression(self):
        result = ParseResult()
        if not self.current_token.matches(GL_KEYWORD, "FOR"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'FOR'",
                )
            )

        start_position = self.current_token.position_start.copy()
        result.register_advancement()
        self.advance()

        if self.current_token.type == GL_LPAREN:
            return self._parse_c_style_for(result, start_position)

        return self._parse_iterator_for(result)
