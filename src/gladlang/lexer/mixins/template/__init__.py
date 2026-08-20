"""Backtick template string lexing (interpolation), composed into a single class."""

from .emit_interpolation import LexerEmitInterpolation
from .lex_interpolation_expression import LexerLexInterpolationExpression
from .make_template_string import LexerMakeTemplateString
from .scan_interpolation_expression import LexerScanInterpolationExpression


class LexerTemplate(
    LexerMakeTemplateString,
    LexerEmitInterpolation,
    LexerScanInterpolationExpression,
    LexerLexInterpolationExpression,
):
    pass


__all__ = ["LexerTemplate"]
