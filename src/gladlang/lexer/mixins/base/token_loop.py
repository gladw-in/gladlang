"""Main tokenization loop that scans source code and produces tokens."""

from gladlang.core.constants import DIGITS
from gladlang.core.constants.token_types import GL_EOF
from gladlang.core.errors import IllegalCharacterError, Position
from gladlang.core.util.settings import Settings
from gladlang.lexer.token import Token

from .simple_tokens import SIMPLE_CHARACTER_TOKENS


class LexerTokenLoop:
    def make_tokens(self):
        if self.source.startswith("\ufeff"):
            self.source = self.source[1:]
            self.position = Position(-1, 0, -1, self.filename, self.source)
            self.current_character = None
            self.advance()

        tokens = []

        while self.current_character is not None:
            if self.current_character in " \t\r\n":
                self.advance()
                continue

            if self.current_character == "#":
                self.skip_comment()
                continue

            if len(tokens) >= Settings.MAX_TOKENS:
                return [], IllegalCharacterError(
                    self.position,
                    self.position,
                    f"Source produces too many tokens (exceeds limit of {Settings.MAX_TOKENS:,})",
                )

            if self.current_character in DIGITS:
                token, error = self.make_number()
                if error:
                    return [], error

                tokens.append(token)
            elif self.current_character.isidentifier():
                tokens.append(self.make_identifier())
            elif self.current_character == '"':
                token = self.make_string()
                if isinstance(token, tuple):
                    return [], token[1]

                tokens.append(token)
            elif self.current_character == "+":
                tokens.append(self._lex_plus())
            elif self.current_character == "-":
                tokens.append(self._lex_minus())
            elif self.current_character == "*":
                tokens.append(self._lex_multiply())
            elif self.current_character == "/":
                tokens.append(self._lex_divide())
            elif self.current_character == "%":
                tokens.append(self._lex_modulo())
            elif self.current_character == "&":
                tokens.append(self._lex_bitwise_and())
            elif self.current_character == "|":
                tokens.append(self._lex_bitwise_or())
            elif self.current_character == "^":
                tokens.append(self._lex_bitwise_xor())
            elif self.current_character == "<":
                tokens.append(self._lex_less_than())
            elif self.current_character == ">":
                tokens.append(self._lex_greater_than())
            elif self.current_character in SIMPLE_CHARACTER_TOKENS:
                tokens.append(
                    Token(
                        SIMPLE_CHARACTER_TOKENS[self.current_character],
                        position_start=self.position,
                    )
                )
                self.advance()
            elif self.current_character == "!":
                token, error = self.make_not_equals()
                if error:
                    return [], error

                tokens.append(token)
            elif self.current_character == "=":
                tokens.append(self.make_equals())
            elif self.current_character == "`":
                result = self.make_template_string()
                if isinstance(result, tuple):
                    return [], result[1]

                if len(tokens) + len(result) > Settings.MAX_TOKENS:
                    return [], IllegalCharacterError(
                        self.position,
                        self.position,
                        f"Source produces too many tokens (exceeds limit of {Settings.MAX_TOKENS:,})",
                    )

                tokens.extend(result)
            else:
                return [], self._lex_illegal_character()

        tokens.append(Token(GL_EOF, position_start=self.position))

        return tokens, None
