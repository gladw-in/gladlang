"""Number arithmetic: division, modulo, floor division."""

from .div import NumberArithmeticDiv
from .floor_div import NumberArithmeticFloorDiv
from .mod import NumberArithmeticMod


class NumberArithmeticDivMod(
    NumberArithmeticDiv,
    NumberArithmeticMod,
    NumberArithmeticFloorDiv,
):
    __slots__ = ()


__all__ = ["NumberArithmeticDivMod"]
