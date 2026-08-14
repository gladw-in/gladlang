"""Core lexer state, position management, and comment skipping."""

from gladlang.core.errors import IllegalCharacterError, Position


class LexerCore:
    def __init__(self, filename, source):
        self.filename = filename
        self.source = source
        self.position = Position(-1, 0, -1, filename, source)
        self.current_character = None
        self.advance()

    def advance(self):
        self.position.advance(self.current_character)
        self.current_character = (
            self.source[self.position.index]
            if self.position.index < len(self.source)
            else None
        )

    def peek(self):
        next_index = self.position.index + 1
        if next_index < len(self.source):
            return self.source[next_index]

        return None

    def skip_comment(self):
        self.advance()
        while self.current_character != "\n" and self.current_character is not None:
            self.advance()

    def _lex_illegal_character(self):
        start_position = self.position.copy()
        illegal_character = self.current_character
        self.advance()
        return IllegalCharacterError(
            start_position, self.position, "'" + illegal_character + "'"
        )
