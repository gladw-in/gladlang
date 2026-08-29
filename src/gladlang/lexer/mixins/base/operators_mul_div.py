"""Lexing for *, **, **=, *=, /, //, //=, /=."""

from gladlang.lexer.token import Token
from gladlang.core.constants.token_types import (
    GL_DIV,
    GL_DIVEQ,
    GL_FLOORDIV,
    GL_FLOORDIVEQ,
    GL_MUL,
    GL_MULEQ,
    GL_POW,
    GL_POWEQ,
)


class LexerOperatorsMulDiv:
    def _lex_mul(self):
        start_position = self.position.copy()
        self.advance()
        if self.current_character == "*":
            self.advance()
            if self.current_character == "=":
                token = Token(
                    GL_POWEQ, position_start=start_position, position_end=self.position
                )
                self.advance()
                return token
            else:
                return Token(
                    GL_POW, position_start=start_position, position_end=self.position
                )
        elif self.current_character == "=":
            token = Token(
                GL_MULEQ, position_start=start_position, position_end=self.position
            )
            self.advance()
            return token
        else:
            return Token(GL_MUL, position_start=start_position)

    def _lex_div(self):
        start_position = self.position.copy()
        self.advance()
        if self.current_character == "/":
            self.advance()
            if self.current_character == "=":
                token = Token(
                    GL_FLOORDIVEQ,
                    position_start=start_position,
                    position_end=self.position,
                )
                self.advance()
                return token
            else:
                return Token(
                    GL_FLOORDIV,
                    position_start=start_position,
                    position_end=self.position,
                )
        elif self.current_character == "=":
            token = Token(
                GL_DIVEQ, position_start=start_position, position_end=self.position
            )
            self.advance()
            return token
        else:
            return Token(GL_DIV, position_start=start_position)
