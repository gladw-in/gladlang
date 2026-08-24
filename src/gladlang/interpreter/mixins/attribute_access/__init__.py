"""Visitors for attribute, list element, and instance creation, composed into a single class."""

from .attribute_access import InterpreterAttributeAccessCore
from .list_access import InterpreterListAccess
from .new_instance import InterpreterNewInstance


class InterpreterAttributeAccess(
    InterpreterAttributeAccessCore,
    InterpreterListAccess,
    InterpreterNewInstance,
):
    pass


__all__ = ["InterpreterAttributeAccess"]
