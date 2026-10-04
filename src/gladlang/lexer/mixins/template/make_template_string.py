"""Scan backtick template strings with escapes and interpolation."""

from gladlang.core.errors import InvalidSyntaxError
from gladlang.core.util.settings import Settings
from gladlang.lexer.token import Token
from gladlang.core.constants.token_types import GL_LPAREN, GL_RPAREN, GL_STRING


class LexerMakeTemplateString:
    def make_template_string(self, _nesting_depth=None):
        if _nesting_depth is None:
            _nesting_depth = getattr(self, "_template_nesting_depth", 0)

        if _nesting_depth >= Settings.MAX_TEMPLATE_DEPTH:
            return [], InvalidSyntaxError(
                self.position.copy(),
                self.position.copy(),
                f"Template string nesting depth exceeds limit ({Settings.MAX_TEMPLATE_DEPTH})",
            )

        tokens = []
        start_position = self.position.copy()
        self.advance()

        tokens.append(Token(GL_LPAREN, position_start=start_position))

        literal_buffer = []
        escape_next = False

        while self.current_character is not None and (
            self.current_character != "`" or escape_next
        ):
            if not escape_next and self.current_character == "$" and self.peek() == "{":
                text_part = "".join(literal_buffer)
                literal_buffer = []

                error = self._emit_interpolation(
                    tokens, text_part, start_position, _nesting_depth
                )

                if error:
                    return [], error

                if len(tokens) >= Settings.MAX_TOKENS:
                    return [], InvalidSyntaxError(
                        start_position,
                        self.position.copy(),
                        f"Source produces too many tokens "
                        f"(exceeds limit of {Settings.MAX_TOKENS:,})",
                    )

            elif escape_next:
                if self.current_character == "n":
                    literal_buffer.append("\n")
                elif self.current_character == "t":
                    literal_buffer.append("\t")
                elif self.current_character == "r":
                    literal_buffer.append("\r")
                elif self.current_character == "`":
                    literal_buffer.append("`")
                elif self.current_character == "\\":
                    literal_buffer.append("\\")
                elif self.current_character == '"':
                    literal_buffer.append('"')
                elif self.current_character == "'":
                    literal_buffer.append("'")
                elif self.current_character == "$":
                    literal_buffer.append("$")
                else:
                    literal_buffer.append(self.current_character)

                escape_next = False
                self.advance()

            elif self.current_character == "\\":
                escape_next = True
                self.advance()

            else:
                literal_buffer.append(self.current_character)
                self.advance()

        text_part = "".join(literal_buffer)

        if self.current_character is None:
            return [], InvalidSyntaxError(
                start_position,
                self.position.copy(),
                "Unterminated template string",
            )

        tokens.append(
            Token(
                GL_STRING,
                text_part,
                position_start=start_position,
                position_end=self.position.copy(),
            )
        )

        tokens.append(Token(GL_RPAREN, position_start=self.position))

        self.advance()

        return tokens
