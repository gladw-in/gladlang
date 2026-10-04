"""Core method for scanning decimal numbers and floats."""


class LexerDecimalFloatCore:
    def _scan_decimal_or_float(self, start_position):
        literal, dots, error = self._scan_decimal_float_body(start_position)
        if error:
            return None, error

        token, error = self._scan_decimal_float_exponent(start_position, literal)
        if error:
            return None, error

        if token is not None:
            return token, None

        return self._finalize_decimal_float(start_position, literal, dots)
