"""Expression-visitor mixins, composed into a single class."""

from .binary_operator import InterpreterBinaryOperator
from .call import InterpreterCall
from .chained_comparison import InterpreterChainedComparison
from .post_operator import InterpreterPostOperator
from .ternary import InterpreterTernary
from .unary_increment_decrement import InterpreterUnaryIncrementDecrement
from .unary_operator import InterpreterUnaryOperator


class InterpreterExpressions(
    InterpreterBinaryOperator,
    InterpreterUnaryOperator,
    InterpreterUnaryIncrementDecrement,
    InterpreterTernary,
    InterpreterChainedComparison,
    InterpreterPostOperator,
    InterpreterCall,
):
    pass


__all__ = ["InterpreterExpressions"]
