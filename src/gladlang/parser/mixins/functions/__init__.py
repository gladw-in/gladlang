"""Function definitions (named and anonymous), composed into a single class."""

from .function_arguments import ParserFunctionArguments
from .function_definition import ParserFunctionDefinition
from .function_name import ParserFunctionName


class ParserFunctions(
    ParserFunctionDefinition,
    ParserFunctionName,
    ParserFunctionArguments,
):
    pass


__all__ = ["ParserFunctions"]
