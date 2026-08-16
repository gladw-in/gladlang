"""Statement-visitor mixins, composed into a single class."""

from .c_for_loop import InterpreterCForLoop
from .conditionals import InterpreterConditionals
from .for_loop import InterpreterForLoop
from .jump_statements import InterpreterJumpStatements
from .loop_iterator import InterpreterLoopIterator
from .loop_unpack import InterpreterLoopUnpack
from .print_statement import InterpreterPrintStatement
from .statement_list import InterpreterStatementList
from .try_catch import InterpreterTryCatch
from .try_catch_body import InterpreterTryCatchBody
from .while_loop import InterpreterWhileLoop


class InterpreterStatements(
    InterpreterStatementList,
    InterpreterConditionals,
    InterpreterLoopUnpack,
    InterpreterLoopIterator,
    InterpreterForLoop,
    InterpreterWhileLoop,
    InterpreterCForLoop,
    InterpreterJumpStatements,
    InterpreterTryCatch,
    InterpreterTryCatchBody,
    InterpreterPrintStatement,
):
    pass


__all__ = ["InterpreterStatements"]
