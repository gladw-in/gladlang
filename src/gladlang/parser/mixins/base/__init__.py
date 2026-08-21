"""Core parser state, token management, nesting depth, top-level parse and composed into a single class."""

from .core import ParserCore
from .nesting_depth import ParserNestingDepth
from .parse import ParserParse
from .statement_list import ParserStatementList


class ParserBase(
    ParserCore,
    ParserNestingDepth,
    ParserParse,
    ParserStatementList,
):
    pass


__all__ = ["ParserBase"]
