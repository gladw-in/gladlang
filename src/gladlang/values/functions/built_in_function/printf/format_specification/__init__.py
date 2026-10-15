"""PRINTF format specification package – combines the mixins."""

from .core import BuiltInFunctionPrintfFormatSpecificationCore
from .int_specification import BuiltInFunctionPrintfFormatSpecificationInt
from .float_specification import BuiltInFunctionPrintfFormatSpecificationFloat

__all__ = ["BuiltInFunctionPrintfFormatSpecification"]


class BuiltInFunctionPrintfFormatSpecification(
    BuiltInFunctionPrintfFormatSpecificationCore,
    BuiltInFunctionPrintfFormatSpecificationInt,
    BuiltInFunctionPrintfFormatSpecificationFloat,
):
    __slots__ = ()
