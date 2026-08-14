"""Number lexer entry: try radix, then decimal/float."""


class LexerMakeNumber:
    def make_number(self):
        start_position = self.position.copy()

        radix_result = self._try_radix_literal(start_position)
        if radix_result is not None:
            return radix_result

        return self._scan_decimal_or_float(start_position)
