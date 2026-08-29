"""RANDOM built-in functions – cryptographically secure RANDOM, RANDOM_FLOAT, and RANDOM_RANGE."""

from .random_float import BuiltInFunctionRandomFloat
from .random_int import BuiltInFunctionRandomInt
from .random_range import BuiltInFunctionRandomRange
from .random_range_validate import BuiltInFunctionRandomRangeValidate


class BuiltInFunctionRandom(
    BuiltInFunctionRandomInt,
    BuiltInFunctionRandomFloat,
    BuiltInFunctionRandomRange,
    BuiltInFunctionRandomRangeValidate,
):
    __slots__ = ()


__all__ = ["BuiltInFunctionRandom"]
