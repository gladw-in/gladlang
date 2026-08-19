"""BoundMethod – wraps a function with an instance (self), with its own TCO trampoline."""

from .core import BoundMethodCore
from .execute import BoundMethodExecute
from .handle_call_outcome import BoundMethodHandleCallOutcome
from .resolve_overload import BoundMethodResolveOverload
from .setup_call_context import BoundMethodSetupCallContext


class BoundMethod(
    BoundMethodExecute,
    BoundMethodResolveOverload,
    BoundMethodSetupCallContext,
    BoundMethodHandleCallOutcome,
    BoundMethodCore,
):
    __slots__ = ()


__all__ = ["BoundMethod"]
