"""Number logical and bitwise operations (shifts are in shifts.py)."""

from .bit_and import NumberBitwiseAnd
from .bit_not import NumberBitwiseNot
from .bit_or import NumberBitwiseOr
from .bit_xor import NumberBitwiseXor
from .logical import NumberBitwiseLogical


class NumberBitwise(
    NumberBitwiseLogical,
    NumberBitwiseAnd,
    NumberBitwiseOr,
    NumberBitwiseXor,
    NumberBitwiseNot,
):
    __slots__ = ()


__all__ = ["NumberBitwise"]
