"""Number arithmetic package – combines add, subtract, and multiply mixins."""

from .add import NumberArithmeticAddSubtractMulAdd
from .subtract import NumberArithmeticAddSubtractMulSubtract
from .multiply import NumberArithmeticAddSubtractMulMultiply

__all__ = ["NumberArithmeticAddSubtractMul"]


class NumberArithmeticAddSubtractMul(
    NumberArithmeticAddSubtractMulAdd,
    NumberArithmeticAddSubtractMulSubtract,
    NumberArithmeticAddSubtractMulMultiply,
):
    __slots__ = ()
