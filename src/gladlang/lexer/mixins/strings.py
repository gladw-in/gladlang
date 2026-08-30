"""Double‑quoted and triple‑quoted string lexing with escape sequences."""

from gladlang.core.errors import InvalidSyntaxError
from gladlang.lexer.token import Token
from gladlang.core.constants.token_types import GL_STRING


class LexerStrings:
    def make_string(self):
        characters = []
        position_start = self.position.copy()
        is_multiline = False

        self.advance()

        if self.current_character == '"' and self.peek() == '"':
            is_multiline = True
            self.advance()
            self.advance()

        escape_character = False

        while self.current_character is not None:
            if escape_character:
                if self.current_character == "n":
                    characters.append("\n")
                elif self.current_character == "t":
                    characters.append("\t")
                elif self.current_character == "r":
                    characters.append("\r")
                elif self.current_character == '"':
                    characters.append('"')
                elif self.current_character == "\\":
                    characters.append("\\")
                elif self.current_character == "0":
                    characters.append("\0")
                elif self.current_character == "u":
                    hex_characters = []
                    for _ in range(4):
                        self.advance()
                        if self.current_character is None:
                            return None, InvalidSyntaxError(
                                position_start,
                                self.position,
                                "Unterminated \\u escape sequence",
                            )

                        hex_characters.append(self.current_character)

                    try:
                        characters.append(chr(int("".join(hex_characters), 16)))
                    except ValueError:
                        return None, InvalidSyntaxError(
                            position_start,
                            self.position,
                            f"Invalid \\u escape: \\u{''.join(hex_characters)}",
                        )
                else:
                    characters.append(self.current_character)

                escape_character = False
            elif self.current_character == "\\":
                escape_character = True
            elif self.current_character == '"':
                if is_multiline:
                    if self.peek() == '"':
                        self.advance()
                        if self.peek() == '"':
                            self.advance()
                            break
                        else:
                            characters.append('""')
                    else:
                        characters.append('"')
                else:
                    break
            else:
                characters.append(self.current_character)

            self.advance()

        if self.current_character is None:
            return None, InvalidSyntaxError(
                position_start, self.position, "Unterminated string literal"
            )

        string_value = "".join(characters)
        self.advance()

        return Token(GL_STRING, string_value, position_start, self.position)
