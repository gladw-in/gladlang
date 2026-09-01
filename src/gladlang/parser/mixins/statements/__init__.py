"""Statement-parsing mixins, composed into a single class."""

from .break_continue import StatementsBreakContinue
from .dispatch import StatementsDispatch
from .for_c_style import StatementsForCStyle
from .for_dispatch import StatementsForDispatch
from .for_iterator import StatementsForIterator
from .if_statement import StatementsIf
from .let_destructure import StatementsLetDestructure
from .let_dispatch import StatementsLetDispatch
from .let_single import StatementsLetSingle
from .print_statement import StatementsPrint
from .return_throw import StatementsReturnThrow
from .visibility import StatementsVisibility
from .while_loop import StatementsWhileLoop


class ParserStatements(
    StatementsDispatch,
    StatementsVisibility,
    StatementsPrint,
    StatementsIf,
    StatementsLetDispatch,
    StatementsLetDestructure,
    StatementsLetSingle,
    StatementsBreakContinue,
    StatementsReturnThrow,
    StatementsWhileLoop,
    StatementsForDispatch,
    StatementsForCStyle,
    StatementsForIterator,
):
    pass


__all__ = ["ParserStatements"]
