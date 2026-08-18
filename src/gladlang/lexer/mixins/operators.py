"""Two‑character operators: !=, ==, and error handling for '!'."""

from gladlang.core.errors import InvalidSyntaxError
from gladlang.lexer.token import Token
from gladlang.core.constants.token_types import GL_NE, GL_EE, GL_EQ


class LexerOperators:
    def make_not_equals(self):
        position_start = self.position.copy()
        self.advance()

        if self.current_character == "=":
            self.advance()
            return (
                Token(GL_NE, position_start=position_start, position_end=self.position),
                None,
            )

        self.advance()

        return None, InvalidSyntaxError(
            position_start, self.position, "Expected '=' after '!'"
        )

    def make_equals(self):
        token_type = GL_EQ
        position_start = self.position.copy()
        self.advance()

        if self.current_character == "=":
            self.advance()
            token_type = GL_EE

        return Token(
            token_type, position_start=position_start, position_end=self.position
        )
