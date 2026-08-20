"""List and dictionary literals, comprehensions, and iteration variable parsing."""

from .comprehension_clauses import ParserComprehensionClauses
from .dict_comprehension import ParserDictComprehension
from .dict_expression import ParserDictExpression
from .dict_plain import ParserDictPlain
from .iterator_variables import ParserIteratorVariables
from .list_comprehension import ParserListComprehension
from .list_expression import ParserListExpression
from .list_plain import ParserListPlain


class ParserCollections(
    ParserIteratorVariables,
    ParserComprehensionClauses,
    ParserListExpression,
    ParserListComprehension,
    ParserListPlain,
    ParserDictExpression,
    ParserDictComprehension,
    ParserDictPlain,
):
    pass


__all__ = ["ParserCollections"]
