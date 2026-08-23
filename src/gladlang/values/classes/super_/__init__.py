"""Super – represents the SUPER keyword for parent method/constructor delegation."""

from .core import SuperCore
from .execute import SuperExecute
from .find_constructor import SuperFindConstructor
from .get_attribute import SuperGetAttribute


class Super(
    SuperGetAttribute,
    SuperExecute,
    SuperFindConstructor,
    SuperCore,
):
    __slots__ = ()


__all__ = ["Super"]
