"""Visitor for unary operators: ++, --, -, NOT, bitwise NOT."""

from gladlang.core.constants import (
    GL_BIT_NOT,
    GL_KEYWORD,
    GL_MINUS,
    GL_MINUSMINUS,
    GL_PLUSPLUS,
)
from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number


class InterpreterUnaryOperator:
    def visit_UnaryOperatorNode(self, node, context):
        if node.operator_token.type in (GL_PLUSPLUS, GL_MINUSMINUS):
            return self._visit_pre_increment_decrement(node, context)

        result = RuntimeResult()

        value = result.register(self.visit(node.node, context))
        if result.error:
            return result

        value = value.copy()
        error = None

        if node.operator_token.type == GL_MINUS:
            if isinstance(value, Number):
                value, error = value.multed_by(Number(-1))
                if error:
                    error.position_start = node.position_start
                    error.position_end = node.position_end
                    error.context = context
            else:
                error = RuntimeError(
                    node.position_start,
                    node.position_end,
                    "Unary '-' can only be applied to numbers",
                    context,
                )

        elif node.operator_token.matches(GL_KEYWORD, "NOT"):
            value, error = value.notted()
            if error:
                error.position_start = node.position_start
                error.position_end = node.position_end
                error.context = context
            else:
                value = (Number.true if value.is_true() else Number.false).copy()

        elif node.operator_token.type == GL_BIT_NOT:
            value, error = value.bitted_not()
            if error:
                error.position_start = node.position_start
                error.position_end = node.position_end
                error.context = context

        if error:
            return result.failure(error)

        return result.success(
            value.set_position(node.position_start, node.position_end)
        )
