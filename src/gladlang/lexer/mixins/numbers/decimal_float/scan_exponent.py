"""Scans the exponent part of a float literal."""

from gladlang.core.constants import DIGITS
from gladlang.core.errors import InvalidSyntaxError


class LexerDecimalFloatScanExponent:
    def _scan_decimal_float_exponent(self, start_position, literal):
        if self.current_character in ("e", "E"):
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

            return self._finite_float_token(literal, start_position)

        return None, None
