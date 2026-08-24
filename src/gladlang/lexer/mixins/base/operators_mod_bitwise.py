"""Lexing for %, %=, &, &=, |, |=, ^, ^=."""

from gladlang.lexer.token import Token
from gladlang.core.constants.token_types import (
    GL_BIT_AND,
    GL_BIT_ANDEQ,
    GL_BIT_OR,
    GL_BIT_OREQ,
    GL_BIT_XOR,
    GL_BIT_XOREQ,
    GL_MOD,
    GL_MODEQ,
)


class LexerOperatorsModBitwise:
    def _lex_mod(self):
        start_position = self.position.copy()
        self.advance()
        if self.current_character == "=":
            token = Token(
                GL_MODEQ, position_start=start_position, position_end=self.position
            )
            self.advance()
            return token
        else:
            return Token(GL_MOD, position_start=start_position)

    def _lex_bit_and(self):
        start_position = self.position.copy()
        self.advance()
        if self.current_character == "=":
            token = Token(
                GL_BIT_ANDEQ, position_start=start_position, position_end=self.position
            )
            self.advance()
            return token
        else:
            return Token(GL_BIT_AND, position_start=start_position)

    def _lex_bit_or(self):
        start_position = self.position.copy()
        self.advance()
        if self.current_character == "=":
            token = Token(
                GL_BIT_OREQ, position_start=start_position, position_end=self.position
            )
            self.advance()
            return token
        else:
            return Token(GL_BIT_OR, position_start=start_position)

    def _lex_bit_xor(self):
        start_position = self.position.copy()
        self.advance()
        if self.current_character == "=":
            token = Token(
                GL_BIT_XOREQ, position_start=start_position, position_end=self.position
            )
            self.advance()
            return token
        else:
            return Token(GL_BIT_XOR, position_start=start_position)
