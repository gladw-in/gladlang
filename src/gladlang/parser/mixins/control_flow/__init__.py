"""SWITCH and TRY/CATCH/FINALLY statement parsing, composed into a single class."""

from .switch_expression import ParserSwitchExpression
from .try_expression import ParserTryExpression


class ParserControlFlow(
    ParserSwitchExpression,
    ParserTryExpression,
):
    pass


__all__ = ["ParserControlFlow"]
