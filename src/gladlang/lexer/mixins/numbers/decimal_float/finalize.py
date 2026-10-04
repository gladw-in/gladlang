"""Finalizes a decimal or float literal after scanning."""


class LexerDecimalFloatFinalize:
    def _finalize_decimal_float(self, start_position, literal, dots):
        literal = literal.replace("_", "")

        if not dots:
            return self._checked_int_token(literal, 10, start_position)
        else:
            return self._finite_float_token(literal, start_position)
