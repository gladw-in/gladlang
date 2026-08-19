"""Number lexing (integers, floats, hex, octal, binary), composed into a single class."""

from .checked_int_token import LexerCheckedIntToken
from .decimal_float import LexerDecimalFloat
from .make_number import LexerMakeNumber
from .radix_literal import LexerRadixLiteral


class LexerNumbers(
    LexerMakeNumber,
    LexerRadixLiteral,
    LexerDecimalFloat,
    LexerCheckedIntToken,
):
    pass


__all__ = ["LexerNumbers"]
