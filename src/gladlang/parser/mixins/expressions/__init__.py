"""Expression-parsing mixins, composed into a single class."""

from .arithmetic import ExpressionsArithmetic
from .assignment import ExpressionsAssignment
from .assignment_target import ExpressionsAssignmentTarget
from .atom import ExpressionsAtom
from .attribute_access import ExpressionsAttributeAccess
from .boolean_expression import ExpressionsBoolean
from .call_arguments import ExpressionsCallArguments
from .call_chain import ExpressionsCallChain
from .subscript_access import ExpressionsSubscriptAccess
from .ternary import ExpressionsTernary


class ParserExpressions(
    ExpressionsAssignment,
    ExpressionsAssignmentTarget,
    ExpressionsTernary,
    ExpressionsBoolean,
    ExpressionsArithmetic,
    ExpressionsCallChain,
    ExpressionsCallArguments,
    ExpressionsAttributeAccess,
    ExpressionsSubscriptAccess,
    ExpressionsAtom,
):
    pass


__all__ = ["ParserExpressions"]
