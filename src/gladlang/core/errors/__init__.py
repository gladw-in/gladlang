"""Error handling package – exposes position, error types, and runtime error classes."""

from .position import Position
from .error import Error
from .illegal_character_error import IllegalCharacterError
from .invalid_syntax_error import InvalidSyntaxError
from .runtime_error import RuntimeError

__all__ = [
    "Position",
    "Error",
    "IllegalCharacterError",
    "InvalidSyntaxError",
    "RuntimeError",
]
