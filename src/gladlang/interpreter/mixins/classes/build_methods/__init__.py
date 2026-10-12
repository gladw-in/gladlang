"""Build class methods from method nodes, grouping overloads and enforcing LSP."""

from .add_overload import InterpreterBuildMethodsAddOverload
from .core import InterpreterBuildMethodsCore
from .create_function import InterpreterBuildMethodsCreateFunction
from .lsp_check import InterpreterBuildMethodsLspCheck
from .merge_inherited import InterpreterBuildMethodsMergeInherited
from .validate_overloads import InterpreterBuildMethodsValidateOverloads


class InterpreterBuildMethods(
    InterpreterBuildMethodsCore,
    InterpreterBuildMethodsCreateFunction,
    InterpreterBuildMethodsAddOverload,
    InterpreterBuildMethodsLspCheck,
    InterpreterBuildMethodsMergeInherited,
    InterpreterBuildMethodsValidateOverloads,
):
    pass


__all__ = ["InterpreterBuildMethods"]
