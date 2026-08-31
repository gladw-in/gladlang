"""Builds an integer token with base and bit-length limit."""

from gladlang.core.errors import InvalidSyntaxError
from gladlang.core.util.settings import Settings
from gladlang.lexer.token import Token
from gladlang.core.constants.token_types import GL_INT


class LexerCheckedIntToken:
    def _checked_int_token(self, digit_string, base, start_position):
        value = int(digit_string, base)
        if value.bit_length() > Settings.MAX_INT_BITS:
            return None, InvalidSyntaxError(
                start_position,
                self.position,
                "Integer literal too large (exceeds integer size limit)",
            )

        return Token(GL_INT, value, start_position, self.position), None
