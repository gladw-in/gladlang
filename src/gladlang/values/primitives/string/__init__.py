"""String – immutable character sequence with concatenation, repetition, and indexing."""

from .arithmetic import StringArithmetic
from .comparisons import StringComparisons
from .core import StringCore
from .element_access import StringElementAccess
from .instanceof import StringInstanceof


class String(
    StringArithmetic,
    StringElementAccess,
    StringComparisons,
    StringInstanceof,
    StringCore,
):
    __slots__ = ()


__all__ = ["String"]
