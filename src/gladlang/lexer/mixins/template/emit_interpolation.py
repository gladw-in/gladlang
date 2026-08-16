"""Emit token sequence for ${...} interpolation segments."""

from gladlang.lexer.token import Token
from gladlang.core.constants.token_types import (
    GL_STRING,
    GL_LPAREN,
    GL_RPAREN,
    GL_PLUS,
    GL_IDENTIFIER,
)


class LexerEmitInterpolation:
    def _emit_interpolation(self, tokens, text_part, start_position, _depth):
        tokens.append(
            Token(
                GL_STRING,
                text_part,
                position_start=start_position,
                position_end=self.position.copy(),
            )
        )

        tokens.append(Token(GL_PLUS, position_start=self.position))
        tokens.append(Token(GL_IDENTIFIER, "STR", position_start=self.position))
        tokens.append(Token(GL_LPAREN, position_start=self.position))

        self.advance()
        self.advance()

        expression_text = self._scan_interpolation_expression()

        inner_tokens, error = self._lex_interpolation_expression(
            expression_text, _depth
        )

        if error:
            return error

        tokens.extend(inner_tokens)

        tokens.append(Token(GL_RPAREN, position_start=self.position))
        tokens.append(Token(GL_PLUS, position_start=self.position))

        return None
