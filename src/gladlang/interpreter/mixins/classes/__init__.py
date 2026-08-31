"""Visitors for class definitions and MRO computation, composed into a single class."""

from .build_methods import InterpreterBuildMethods
from .class_node import InterpreterClassNode
from .compute_mro import InterpreterComputeMro
from .resolve_superclasses import InterpreterResolveSuperclasses


class InterpreterClasses(
    InterpreterClassNode,
    InterpreterResolveSuperclasses,
    InterpreterBuildMethods,
    InterpreterComputeMro,
):
    pass


__all__ = ["InterpreterClasses"]
