"""Lexer decimal and float package – combines the mixins."""

from .core import LexerDecimalFloatCore
from .scan_body import LexerDecimalFloatScanBody
from .scan_exponent import LexerDecimalFloatScanExponent
from .finalize import LexerDecimalFloatFinalize
from .finite_float_token import LexerDecimalFloatFiniteFloatToken

__all__ = ["LexerDecimalFloat"]


class LexerDecimalFloat(
    LexerDecimalFloatCore,
    LexerDecimalFloatScanBody,
    LexerDecimalFloatScanExponent,
    LexerDecimalFloatFinalize,
    LexerDecimalFloatFiniteFloatToken,
):
    pass
