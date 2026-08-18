"""Lexes a decimal numbers and floats with underscores and exponent notation."""

from gladlang.core.constants import DIGITS
from gladlang.core.errors import InvalidSyntaxError
from gladlang.lexer.token import Token
from gladlang.core.constants.token_types import GL_FLOAT


class LexerDecimalFloat:
    def _scan_decimal_or_float(self, start_position):
        literal = ""
        dots = 0
        has_exponent = False

        while (
            self.current_character is not None
            and self.current_character in DIGITS + "._"
        ):
            if self.current_character == "_":
                self.advance()
                if (
                    self.current_character is None
                    or self.current_character not in DIGITS + "."
                ):
                    return None, InvalidSyntaxError(
                        start_position,
                        self.position,
                        "Invalid numeric literal: '_' must be between digits",
                    )

                continue

            if self.current_character == ".":
                if dots == 1:
                    break

                if has_exponent:
                    return None, InvalidSyntaxError(
                        start_position,
                        self.position,
                        "Invalid numeric literal: '.' after exponent",
                    )

                dots += 1
                literal += "."
            else:
                literal += self.current_character
            self.advance()

        if self.current_character in ("e", "E"):
            has_exponent = True
            literal += self.current_character
            self.advance()
            if self.current_character in ("+", "-"):
                literal += self.current_character
                self.advance()

            if self.current_character is None or self.current_character not in DIGITS:
                return None, InvalidSyntaxError(
                    start_position,
                    self.position,
                    "Invalid scientific notation: expected digits after exponent",
                )

            while (
                self.current_character is not None and self.current_character in DIGITS
            ):
                literal += self.current_character
                self.advance()

            return Token(GL_FLOAT, float(literal), start_position, self.position), None

        literal = literal.replace("_", "")

        if not dots:
            return self._checked_int_token(literal, 10, start_position)
        else:
            return Token(GL_FLOAT, float(literal), start_position, self.position), None
