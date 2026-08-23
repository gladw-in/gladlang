"""LET statement entry point – dispatches to destructuring or single-variable assignment."""

from gladlang.core.constants import GL_IDENTIFIER, GL_LSQUARE
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.parse_result import ParseResult


class StatementsLetDispatch:
    def _parse_let_statement(self):
        result = ParseResult()

        result.register_advancement()
        self.advance()

        if self.current_token.type == GL_LSQUARE:
            return self._parse_let_destructure(result)

        if self.current_token.type == GL_IDENTIFIER:
            return self._parse_let_single(result)

        return result.failure(
            InvalidSyntaxError(
                self.current_token.position_start,
                self.current_token.position_end,
                "Expected identifier or '['",
            )
        )
