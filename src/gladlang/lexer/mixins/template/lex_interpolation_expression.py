"""Lex interpolation expressions with a fresh Lexer and offset errors."""

from gladlang.core.errors import InvalidSyntaxError
from gladlang.core.util.settings import Settings
from gladlang.core.constants.token_types import GL_EOF


class LexerLexInterpolationExpression:
    def _compute_interp_start_position(self, expression_text):
        start_index = self.position.index - len(expression_text) - 2
        start_line = self.position.line
        column = self.position.column

        for character in expression_text:
            if character == "\n":
                column = 0
            else:
                column -= 1

        start_column = max(0, column - 2)

        return start_index, start_line, start_column

    def _lex_interpolation_expression(self, expression_text, _depth):
        from gladlang.lexer.lexer import Lexer

        (
            start_index,
            start_line,
            start_column,
        ) = self._compute_interp_start_position(expression_text)

        if len(expression_text) > Settings.MAX_INTERPOLATION_SIZE:
            return None, InvalidSyntaxError(
                self.position.copy(),
                self.position.copy(),
                f"Interpolation expression too large (limit {Settings.MAX_INTERPOLATION_SIZE})",
            )

        inner_lexer = Lexer(self.filename, expression_text)
        inner_lexer._template_depth = _depth + 1
        inner_tokens, error = inner_lexer.make_tokens()

        if error:
            if error.position_start is not None:
                error.position_start.index += start_index
                error.position_start.column += start_column

                if not error.position_start.line:
                    error.position_start.line = start_line

                error.position_end = error.position_start.copy()

            return None, error

        if inner_tokens and inner_tokens[-1].type == GL_EOF:
            inner_tokens.pop()

        return inner_tokens, None
