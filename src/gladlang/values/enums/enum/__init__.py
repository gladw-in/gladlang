"""Enum – represents a declared enum type with named cases."""

from .attribute_access import EnumAttributeAccess
from .comparisons import EnumComparisons
from .core import EnumCore
from .instanceof import EnumInstanceof


class Enum(
    EnumAttributeAccess,
    EnumComparisons,
    EnumInstanceof,
    EnumCore,
):
    __slots__ = ()


__all__ = ["Enum"]
