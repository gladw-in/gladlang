"""FunctionGroup – manages overloaded functions (same name, different argument_count)."""

from .add_function import FunctionGroupAddFunction
from .bind_to_instance import FunctionGroupBindToInstance
from .copy import FunctionGroupCopy
from .core import FunctionGroupCore
from .execute import FunctionGroupExecute
from .notted import FunctionGroupNotted


class FunctionGroup(
    FunctionGroupAddFunction,
    FunctionGroupExecute,
    FunctionGroupNotted,
    FunctionGroupBindToInstance,
    FunctionGroupCopy,
    FunctionGroupCore,
):
    __slots__ = ()


__all__ = ["FunctionGroup"]
