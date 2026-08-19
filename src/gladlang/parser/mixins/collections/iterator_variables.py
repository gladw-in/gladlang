"""Parse FOR loop variables: single identifier or destructuring list."""

from gladlang.core.constants import GL_COMMA, GL_IDENTIFIER, GL_LSQUARE, GL_RSQUARE
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.parse_result import ParseResult


class ParserIteratorVariables:
    def parse_iterator_variables(self):
        variable_tokens = []
        result = ParseResult()

        if self.current_token.type == GL_LSQUARE:
            result.register_advancement()
            self.advance()

            if self.current_token.type == GL_IDENTIFIER:
                variable_tokens.append(self.current_token)
                result.register_advancement()
                self.advance()

                while self.current_token.type == GL_COMMA:
                    result.register_advancement()
                    self.advance()
                    if self.current_token.type != GL_IDENTIFIER:
                        return None, result.failure(
                            InvalidSyntaxError(
                                self.current_token.position_start,
                                self.current_token.position_end,
                                "Expected identifier",
                            )
                        )

                    variable_tokens.append(self.current_token)
                    result.register_advancement()
                    self.advance()

            if self.current_token.type != GL_RSQUARE:
                return None, result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected ']'",
                    )
                )

            result.register_advancement()
            self.advance()

            return variable_tokens, result

        elif self.current_token.type == GL_IDENTIFIER:
            variable_tokens.append(self.current_token)
            result.register_advancement()
            self.advance()

            return variable_tokens, result

        return None, None
