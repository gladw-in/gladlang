"""Runtime value system – all GladLang data types and their operations."""

from .primitives.number import Number
from .primitives.string import String
from .primitives.list import List
from .primitives.dict import Dict
from .nulls.frozen_null import FrozenNull
from .nulls.mutable_null import MutableNull
from .nulls.tailcall import TailCall
from .functions.base_function import BaseFunction
from .functions.function import Function
from .functions.function_group import FunctionGroup
from .functions.bound_method import BoundMethod
from .functions.built_in_function import BuiltInFunction
from .classes.class_ import Class
from .classes.instance_ import Instance
from .classes.super_ import Super
from .classes.type_ import Type
from .enums.enum import Enum

Number.false = FrozenNull(0, is_null=False)
Number.true = FrozenNull(1, is_null=False)
Number.null = FrozenNull(0, is_null=True)


__all__ = [
    "Number",
    "String",
    "List",
    "Dict",
    "FrozenNull",
    "MutableNull",
    "TailCall",
    "BaseFunction",
    "Function",
    "FunctionGroup",
    "BoundMethod",
    "BuiltInFunction",
    "Class",
    "Instance",
    "Super",
    "Type",
    "Enum",
]
