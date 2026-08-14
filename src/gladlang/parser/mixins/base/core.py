"""Core parser state and token-cursor advancement."""


class ParserCore:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.loop_count = 0
        self.function_count = 0
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]

        return self.current_token
