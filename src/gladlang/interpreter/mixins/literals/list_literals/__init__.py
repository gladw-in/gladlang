"""List literals package – combines the list literal mixins."""

from .list_literal import InterpreterListLiteralsListLiteral
from .list_comprehension import InterpreterListLiteralsListComprehension

__all__ = ["InterpreterListLiterals"]


class InterpreterListLiterals(
    InterpreterListLiteralsListLiteral,
    InterpreterListLiteralsListComprehension,
):
    pass
