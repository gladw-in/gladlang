"""Lexing for <, <<, <<=, <=, >, >>, >>=, >=."""

from gladlang.lexer.token import Token
from gladlang.core.constants.token_types import (
    GL_GT,
    GL_GTE,
    GL_LSHIFT,
    GL_LSHIFTEQ,
    GL_LT,
    GL_LTE,
    GL_RSHIFT,
    GL_RSHIFTEQ,
)


class LexerOperatorsShiftCompare:
    def _lex_lt(self):
        start_position = self.position.copy()
        self.advance()
        if self.current_character == "<":
            self.advance()
            if self.current_character == "=":
                token = Token(
                    GL_LSHIFTEQ,
                    position_start=start_position,
                    position_end=self.position,
                )
                self.advance()
                return token
            else:
                return Token(
                    GL_LSHIFT, position_start=start_position, position_end=self.position
                )
        elif self.current_character == "=":
            token = Token(
                GL_LTE, position_start=start_position, position_end=self.position
            )
            self.advance()
            return token
        else:
            return Token(GL_LT, position_start=start_position)

    def _lex_gt(self):
        start_position = self.position.copy()
        self.advance()
        if self.current_character == ">":
            self.advance()
            if self.current_character == "=":
                token = Token(
                    GL_RSHIFTEQ,
                    position_start=start_position,
                    position_end=self.position,
                )
                self.advance()
                return token
            else:
                return Token(
                    GL_RSHIFT, position_start=start_position, position_end=self.position
                )
        elif self.current_character == "=":
            token = Token(
                GL_GTE, position_start=start_position, position_end=self.position
            )
            self.advance()
            return token
        else:
            return Token(GL_GT, position_start=start_position)
