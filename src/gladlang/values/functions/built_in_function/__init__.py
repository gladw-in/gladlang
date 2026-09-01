"""BuiltInFunction – implements native functions like INPUT, STR, INT, FLOAT, BOOL, LEN."""

from .bool_function import BuiltInFunctionBool
from .core import BuiltInFunctionCore
from .dispatch import BuiltInFunctionDispatch
from .float_function import BuiltInFunctionFloat
from .input_string import BuiltInFunctionInputString
from .int_function import BuiltInFunctionInt
from .len_function import BuiltInFunctionLen
from .printf import BuiltInFunctionPrintf
from .random import BuiltInFunctionRandom
from .system import BuiltInFunctionSystem
from .time import BuiltInFunctionTime


class BuiltInFunction(
    BuiltInFunctionDispatch,
    BuiltInFunctionInputString,
    BuiltInFunctionInt,
    BuiltInFunctionFloat,
    BuiltInFunctionBool,
    BuiltInFunctionLen,
    BuiltInFunctionPrintf,
    BuiltInFunctionTime,
    BuiltInFunctionRandom,
    BuiltInFunctionSystem,
    BuiltInFunctionCore,
):
    __slots__ = ()


__all__ = ["BuiltInFunction"]
