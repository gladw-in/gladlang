"""Invalid syntax error – raised when the parser detects a grammar violation."""

from .error import Error


class InvalidSyntaxError(Error):
    def __init__(self, position_start, position_end, details=""):
        super().__init__(position_start, position_end, "Invalid Syntax", details)
