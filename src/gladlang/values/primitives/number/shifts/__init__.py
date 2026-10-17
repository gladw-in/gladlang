"""Number shifts package – combines the left and right shift mixins."""

from .left_shift import NumberShiftsLeftShift
from .right_shift import NumberShiftsRightShift

__all__ = ["NumberShifts"]


class NumberShifts(NumberShiftsLeftShift, NumberShiftsRightShift):
    __slots__ = ()
