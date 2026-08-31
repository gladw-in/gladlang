"""Lexes radix-prefixed integer literals (0x, 0o, 0b)."""

from gladlang.core.constants import DIGITS
from gladlang.core.errors import IllegalCharacterError


class LexerRadixLiteral:
    def _try_radix_literal(self, start_position):
        if self.current_character != "0":
            return None

        next_character = self.peek()

        if next_character in ("x", "X"):
            allowed_characters, base, label = DIGITS + "abcdefABCDEF", 16, "hex"
        elif next_character in ("o", "O"):
            allowed_characters, base, label = "01234567", 8, "octal"
        elif next_character in ("b", "B"):
            allowed_characters, base, label = "01", 2, "binary"
        else:
            return None

        self.advance()
        self.advance()

        digits = ""
        while self.current_character is not None:
            if self.current_character == "_":
                self.advance()
                continue

            if self.current_character in allowed_characters:
                digits += self.current_character
                self.advance()
            else:
                break

        if not digits:
            return None, IllegalCharacterError(
                start_position, self.position, f"Invalid {label} literal"
            )

        return self._checked_int_token(digits, base, start_position)
