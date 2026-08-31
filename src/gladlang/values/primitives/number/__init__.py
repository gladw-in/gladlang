"""Number – numeric type (int/float) with arithmetic, bitwise, and comparison operations."""

from .arithmetic_add_subtract_mul import NumberArithmeticAddSubtractMul
from .arithmetic_div_mod import NumberArithmeticDivMod
from .arithmetic_pow import NumberArithmeticPow
from .bitwise import NumberBitwise
from .comparisons import NumberComparisons
from .core import NumberCore
from .instanceof import NumberInstanceof
from .shifts import NumberShifts


class Number(
    NumberArithmeticAddSubtractMul,
    NumberArithmeticDivMod,
    NumberArithmeticPow,
    NumberComparisons,
    NumberBitwise,
    NumberShifts,
    NumberInstanceof,
    NumberCore,
):
    __slots__ = ()


Number.false = None
Number.true = None
Number.null = None


__all__ = ["Number"]
