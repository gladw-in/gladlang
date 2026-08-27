"""Identifier and keyword lexing."""

from gladlang.core.constants import KEYWORDS
from gladlang.lexer.token import Token
from gladlang.core.constants.token_types import GL_KEYWORD, GL_IDENTIFIER


class LexerIdentifiers:
    def make_identifier(self):
        identifier_text = ""
        position_start = self.position.copy()

        while self.current_character is not None and (
            identifier_text == ""
            and self.current_character.isidentifier()
            or identifier_text != ""
            and ("a" + self.current_character).isidentifier()
        ):
            identifier_text += self.current_character
            self.advance()

        token_type = GL_KEYWORD if identifier_text in KEYWORDS else GL_IDENTIFIER

        return Token(token_type, identifier_text, position_start, self.position)
