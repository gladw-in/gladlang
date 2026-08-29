"""Lexing for +, ++, +=, -, --, -=."""

from gladlang.lexer.token import Token
from gladlang.core.constants.token_types import (
    GL_MINUS,
    GL_MINUSEQ,
    GL_MINUSMINUS,
    GL_PLUS,
    GL_PLUSEQ,
    GL_PLUSPLUS,
)


class LexerOperatorsPlusMinus:
    def _lex_plus(self):
        start_position = self.position.copy()
        self.advance()
        if self.current_character == "+":
            token = Token(
                GL_PLUSPLUS, position_start=start_position, position_end=self.position
            )
            self.advance()
            return token
        elif self.current_character == "=":
            token = Token(
                GL_PLUSEQ, position_start=start_position, position_end=self.position
            )
            self.advance()
            return token
        else:
            return Token(GL_PLUS, position_start=start_position)

    def _lex_minus(self):
        start_position = self.position.copy()
        self.advance()
        if self.current_character == "-":
            token = Token(
                GL_MINUSMINUS, position_start=start_position, position_end=self.position
            )
            self.advance()
            return token
        elif self.current_character == "=":
            token = Token(
                GL_MINUSEQ, position_start=start_position, position_end=self.position
            )
            self.advance()
            return token
        else:
            return Token(GL_MINUS, position_start=start_position)
