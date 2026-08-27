"""BaseFunction – abstract base for all callable values (functions, methods, classes)."""

from .arguments import BaseFunctionArguments
from .comparisons import BaseFunctionComparisons
from .core import BaseFunctionCore
from .generate_context import BaseFunctionGenerateContext
from .instanceof import BaseFunctionInstanceof
from .protocol_stubs import BaseFunctionProtocolStubs


class BaseFunction(
    BaseFunctionGenerateContext,
    BaseFunctionComparisons,
    BaseFunctionInstanceof,
    BaseFunctionArguments,
    BaseFunctionProtocolStubs,
    BaseFunctionCore,
):
    __slots__ = ()


__all__ = ["BaseFunction"]
