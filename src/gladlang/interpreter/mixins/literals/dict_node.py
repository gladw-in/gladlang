"""Visitor for dict literals."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.dict import Dict
from gladlang.values.primitives.number import Number
from gladlang.values.primitives.string import String


class InterpreterDictNode:
    def visit_DictNode(self, node, context):
        result = RuntimeResult()

        elements = {}
        for key_expression, value_expression in node.key_value_pairs:
            key = result.register(self.visit(key_expression, context))
            if result.error:
                return result

            value = result.register(self.visit(value_expression, context))
            if result.error:
                return result

            if isinstance(key, (Number, String)):
                elements[key.value] = value
            else:
                return result.failure(
                    RuntimeError(
                        key_expression.position_start,
                        key_expression.position_end,
                        "Dictionary key must be a Number or String",
                        context,
                    )
                )

        return result.success(
            Dict(elements)
            .set_context(context)
            .set_position(node.position_start, node.position_end)
        )
