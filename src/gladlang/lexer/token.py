"""Token class – stores token type, value, and source position."""


class Token:
    __slots__ = ("type", "value", "position_start", "position_end")

    def __init__(
        self, token_type, token_value=None, position_start=None, position_end=None
    ):
        self.type = token_type
        self.value = token_value

        if position_start:
            self.position_start = position_start.copy()
            self.position_end = position_start.copy()
            self.position_end.advance()

        if position_end:
            self.position_end = position_end.copy()

    def matches(self, token_type, token_value):
        return self.type == token_type and self.value == token_value

    def __repr__(self):
        if self.value is not None:
            return f"{self.type}:{self.value}"

        return f"{self.type}"
