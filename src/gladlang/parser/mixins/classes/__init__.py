"""Class declaration and NEW-instantiation parsing, composed into a single class."""

from .class_body import ParserClassBody
from .class_definition import ParserClassDefinition
from .class_field import ParserClassField
from .class_method import ParserClassMethod
from .class_superclasses import ParserClassSuperclasses
from .new_instance import ParserNewInstance


class ParserClasses(
    ParserClassDefinition,
    ParserClassSuperclasses,
    ParserClassBody,
    ParserClassMethod,
    ParserClassField,
    ParserNewInstance,
):
    pass


__all__ = ["ParserClasses"]
