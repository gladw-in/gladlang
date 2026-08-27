"""Class – represents user-defined classes with methods, inheritance, and MRO."""

from .core import ClassCore
from .get_attribute import ClassGetAttribute
from .get_attribute_cache import ClassGetAttributeCache
from .get_attribute_method import ClassGetAttributeMethod
from .get_attribute_static_field import ClassGetAttributeStaticField
from .instantiate import ClassInstantiate
from .set_attribute import ClassSetAttribute


class Class(
    ClassInstantiate,
    ClassSetAttribute,
    ClassGetAttribute,
    ClassGetAttributeCache,
    ClassGetAttributeStaticField,
    ClassGetAttributeMethod,
    ClassCore,
):
    __slots__ = ()


__all__ = ["Class"]
