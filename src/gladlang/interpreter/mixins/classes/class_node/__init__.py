"""Visitor for CLASS declarations: builds the Class value, computes its MRO, evaluates static fields, and builds its methods."""

from .check_depth import InterpreterClassNodeCheckDepth
from .core import InterpreterClassNodeCore
from .create_class import InterpreterClassNodeCreateClass
from .field_conflicts import InterpreterClassNodeFieldConflicts
from .method_conflicts import InterpreterClassNodeMethodConflicts
from .register_class import InterpreterClassNodeRegisterClass
from .static_fields import InterpreterClassNodeStaticFields
from .validate_name import InterpreterClassNodeValidateName


class InterpreterClassNode(
    InterpreterClassNodeCore,
    InterpreterClassNodeValidateName,
    InterpreterClassNodeCheckDepth,
    InterpreterClassNodeCreateClass,
    InterpreterClassNodeStaticFields,
    InterpreterClassNodeMethodConflicts,
    InterpreterClassNodeFieldConflicts,
    InterpreterClassNodeRegisterClass,
):
    pass


__all__ = ["InterpreterClassNode"]
