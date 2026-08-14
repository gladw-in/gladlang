"""Dict – key-value store with size limit and deep copy semantics."""

from .arithmetic import DictArithmetic
from .comparisons import DictComparisons
from .copy import DictCopy
from .core import DictCore
from .element_access import DictElementAccess
from .instanceof import DictInstanceof
from .to_string import DictToString


class Dict(
    DictCopy,
    DictArithmetic,
    DictElementAccess,
    DictComparisons,
    DictInstanceof,
    DictToString,
    DictCore,
):
    __slots__ = ()


__all__ = ["Dict"]
