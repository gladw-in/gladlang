"""PRINT / PRINTLN statement parsing package."""

from .lookahead import StatementsPrintLookahead
from .parse import StatementsPrintParse

__all__ = ["StatementsPrint"]


class StatementsPrint(StatementsPrintLookahead, StatementsPrintParse):
    pass
