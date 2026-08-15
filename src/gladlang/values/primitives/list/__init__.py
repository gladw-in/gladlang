"""List – ordered collection with concatenation, repetition, indexing, and size limit."""

from .arithmetic import ListArithmetic
from .comparisons import ListComparisons
from .copy import ListCopy
from .core import ListCore
from .element_access import ListElementAccess
from .instanceof import ListInstanceof
from .to_string import ListToString


class List(
    ListCopy,
    ListArithmetic,
    ListElementAccess,
    ListComparisons,
    ListInstanceof,
    ListToString,
    ListCore,
):
    __slots__ = ()


__all__ = ["List"]
