"""Type – runtime type objects (Number, String, List, Dict, etc.)."""

from gladlang.values.value import Value

from .comparisons import TypeComparisons
from .core import TypeCore
from .logic_operators import TypeLogicOperators
from .protocol_stubs import TypeProtocolStubs


class Type(
    TypeProtocolStubs,
    TypeComparisons,
    TypeLogicOperators,
    TypeCore,
    Value,
):
    __slots__ = ("name",)


__all__ = ["Type"]
