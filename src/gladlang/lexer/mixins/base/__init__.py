"""Lexer base mixins, composed into a single class."""

from .core import LexerCore
from .operators_mod_bitwise import LexerOperatorsModBitwise
from .operators_mul_div import LexerOperatorsMulDiv
from .operators_plus_minus import LexerOperatorsPlusMinus
from .operators_shift_compare import LexerOperatorsShiftCompare
from .token_loop import LexerTokenLoop


class LexerBase(
    LexerCore,
    LexerOperatorsPlusMinus,
    LexerOperatorsMulDiv,
    LexerOperatorsModBitwise,
    LexerOperatorsShiftCompare,
    LexerTokenLoop,
):
    pass


__all__ = ["LexerBase"]
