"""Visitors for the two simplest literals: numbers and strings."""

from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number
from gladlang.values.primitives.string import String


class InterpreterAtomLiterals:
    def visit_NumberNode(self, number_node, context):
        return RuntimeResult().success(
            Number(number_node.token.value)
            .set_context(context)
            .set_position(number_node.position_start, number_node.position_end)
        )

    def visit_StringNode(self, string_node, context):
        return RuntimeResult().success(
            String(string_node.token.value)
            .set_context(context)
            .set_position(string_node.position_start, string_node.position_end)
        )
