"""Visitors for variable access, assignment, destructuring, visibility and composed into a single class."""

from .multi_variable_assign import InterpreterMultiVariableAssign
from .variable_access import InterpreterVariableAccess
from .variable_assign import InterpreterVariableAssign
from .visibility_statement import InterpreterVisibilityStatement


class InterpreterVariables(
    InterpreterVariableAccess,
    InterpreterVariableAssign,
    InterpreterMultiVariableAssign,
    InterpreterVisibilityStatement,
):
    pass


__all__ = ["InterpreterVariables"]
