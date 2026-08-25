"""ParseResult – accumulates parser state and error information during parsing."""


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, other_result):
        self.advance_count += other_result.advance_count
        if other_result.error:
            self.error = other_result.error

        return other_result.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or not self.advance_count:
            self.error = error

        return self
