"""Creates a finite float token from a literal."""

import math

from gladlang.core.errors import InvalidSyntaxError
from gladlang.lexer.token import Token
from gladlang.core.constants.token_types import GL_FLOAT


class LexerDecimalFloatFiniteFloatToken:
    def _finite_float_token(self, literal, start_position):
        try:
            value = float(literal)
        except (ValueError, OverflowError):
            return None, InvalidSyntaxError(
                start_position,
                self.position,
                "Invalid floating-point literal",
            )

        if not math.isfinite(value):
            return None, InvalidSyntaxError(
                start_position,
                self.position,
                "Floating-point literal is not finite",
            )

        return Token(GL_FLOAT, value, start_position, self.position), None
