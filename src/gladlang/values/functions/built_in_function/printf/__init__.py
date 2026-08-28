"""PRINTF built-in function – formatted string output with %s, %d, %f, and %%."""

from .core import BuiltInFunctionPrintfCore
from .format_specification import BuiltInFunctionPrintfFormatSpecification
from .validate import BuiltInFunctionPrintfValidate


class BuiltInFunctionPrintf(
    BuiltInFunctionPrintfCore,
    BuiltInFunctionPrintfFormatSpecification,
    BuiltInFunctionPrintfValidate,
):
    __slots__ = ()


__all__ = ["BuiltInFunctionPrintf"]
