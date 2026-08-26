"""Value – base class defining the interface for all GladLang runtime objects."""

from .comparison_derived import ValueComparisonDerived
from .core import ValueCore
from .instanceof import ValueInstanceof
from .logic_operators import ValueLogicOperators
from .protocol_stubs import ValueProtocolStubs


class Value(
    ValueProtocolStubs,
    ValueComparisonDerived,
    ValueLogicOperators,
    ValueInstanceof,
    ValueCore,
):
    __slots__ = ()


__all__ = ["Value"]
