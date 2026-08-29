"""Parse optional function name and check for '('."""

from gladlang.core.constants import GL_IDENTIFIER, GL_LPAREN
from gladlang.core.errors import InvalidSyntaxError


class ParserFunctionName:
    def _parse_function_name(self, result):
        if self.current_token.type == GL_IDENTIFIER:
            name_token = self.current_token
            result.register_advancement()
            self.advance()
            if self.current_token.type != GL_LPAREN:
                result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected '(' after function name",
                    )
                )
                return None

            return name_token
        else:
            if self.current_token.type != GL_LPAREN:
                result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected '('",
                    )
                )
                return None

            return None
