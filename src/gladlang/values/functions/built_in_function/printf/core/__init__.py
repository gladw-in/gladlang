"""PRINTF core package – combines the printf mixins."""

from .execute import BuiltInFunctionPrintfCoreExecute
from .build_output import BuiltInFunctionPrintfCoreBuildOutput
from .parse_precision import BuiltInFunctionPrintfCoreParsePrecision
from .handle_specifier import BuiltInFunctionPrintfCoreHandleSpecifier
from .append_output import BuiltInFunctionPrintfCoreAppendOutput

__all__ = ["BuiltInFunctionPrintfCore"]


class BuiltInFunctionPrintfCore(
    BuiltInFunctionPrintfCoreExecute,
    BuiltInFunctionPrintfCoreBuildOutput,
    BuiltInFunctionPrintfCoreParsePrecision,
    BuiltInFunctionPrintfCoreHandleSpecifier,
    BuiltInFunctionPrintfCoreAppendOutput,
):
    __slots__ = ()
