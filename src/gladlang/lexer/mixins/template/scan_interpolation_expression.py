"""Scan inner expression of ${...} interpolation."""


class LexerScanInterpolationExpression:
    def _scan_interpolation_expression(self):
        expression_text = ""
        brace_depth = 1
        inside_string = False
        escape_next = False

        while self.current_character is not None and brace_depth > 0:
            character = self.current_character

            if escape_next:
                expression_text += character
                escape_next = False
            elif character == "\\" and inside_string:
                expression_text += character
                escape_next = True
            elif character == '"':
                inside_string = not inside_string
                expression_text += character
            elif not inside_string:
                if character == "{":
                    brace_depth += 1
                elif character == "}":
                    brace_depth -= 1

                if brace_depth > 0:
                    expression_text += character

            else:
                expression_text += character

            self.advance()

        return expression_text
