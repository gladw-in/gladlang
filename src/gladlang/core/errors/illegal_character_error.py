"""Illegal character error – raised when the lexer encounters an invalid character."""

from .error import Error


class IllegalCharacterError(Error):
    def __init__(self, position_start, position_end, details):
        super().__init__(position_start, position_end, "Illegal Character", details)
