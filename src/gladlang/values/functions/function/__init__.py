"""Function – user-defined function with closure capture, recursion, and TCO."""

from .core import FunctionCore
from .execute import FunctionExecute
from .handle_call_outcome import FunctionHandleCallOutcome
from .resolve_overload import FunctionResolveOverload
from .setup_call_context import FunctionSetupCallContext


class Function(
    FunctionExecute,
    FunctionResolveOverload,
    FunctionSetupCallContext,
    FunctionHandleCallOutcome,
    FunctionCore,
):
    __slots__ = ()


__all__ = ["Function"]
