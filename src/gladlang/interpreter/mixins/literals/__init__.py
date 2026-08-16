"""Visitors for literal values and comprehensions, composed into a single class."""

from .atoms import InterpreterAtomLiterals
from .dict_comprehension import InterpreterDictComprehension
from .dict_node import InterpreterDictNode
from .list_literals import InterpreterListLiterals


class InterpreterLiterals(
    InterpreterAtomLiterals,
    InterpreterListLiterals,
    InterpreterDictNode,
    InterpreterDictComprehension,
):
    pass


__all__ = ["InterpreterLiterals"]
