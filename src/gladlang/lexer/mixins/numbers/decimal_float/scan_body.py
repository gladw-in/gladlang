"""Scans the main body of a decimal or float literal."""

from gladlang.core.constants import DIGITS
from gladlang.core.errors import InvalidSyntaxError


class LexerDecimalFloatScanBody:
    def _scan_decimal_float_body(self, start_position):
        literal = ""
        dots = 0
        has_exponent = False
        previous_was_digit = False

        while (
            self.current_character is not None
            and self.current_character in DIGITS + "._"
        ):
            if self.current_character == "_":
                if not previous_was_digit:
                    return (
                        None,
                        None,
                        InvalidSyntaxError(
                            start_position,
                            self.position,
                            "Invalid numeric literal: '_' must be between digits",
                        ),
                    )

                self.advance()
                if (
                    self.current_character is None
                    or self.current_character not in DIGITS
                ):
                    return (
                        None,
                        None,
                        InvalidSyntaxError(
                            start_position,
                            self.position,
                            "Invalid numeric literal: '_' must be between digits",
                        ),
                    )

                previous_was_digit = False
                continue

            if self.current_character == ".":
                if dots == 1:
                    break

                if has_exponent:
                    return (
                        None,
                        None,
                        InvalidSyntaxError(
                            start_position,
                            self.position,
                            "Invalid numeric literal: '.' after exponent",
                        ),
                    )

                dots += 1
                literal += "."
                previous_was_digit = False
            else:
                literal += self.current_character
                previous_was_digit = True

            self.advance()

        return literal, dots, None
