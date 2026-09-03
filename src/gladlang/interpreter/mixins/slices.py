"""Visitor for slicing operations on lists and strings."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number
from gladlang.values.primitives.string import String
from gladlang.values.primitives.list import List


class InterpreterSlices:
    def visit_SliceAccessNode(self, node, context):
        result = RuntimeResult()

        object_to_slice = result.register(self.visit(node.node_to_slice, context))
        if result.error:
            return result

        start_index = 0
        if node.start_node is not None:
            start_value = result.register(self.visit(node.start_node, context))
            if result.error:
                return result

            if not isinstance(start_value, Number) or (
                hasattr(start_value, "_is_null") and start_value._is_null
            ):
                return result.failure(
                    RuntimeError(
                        node.start_node.position_start,
                        node.start_node.position_end,
                        "Start index must be a number",
                        context,
                    )
                )

            start_index = int(start_value.value)

        end_index = None
        if node.end_node:
            end_value = result.register(self.visit(node.end_node, context))
            if result.error:
                return result

            if not isinstance(end_value, Number) or (
                hasattr(end_value, "_is_null") and end_value._is_null
            ):
                return result.failure(
                    RuntimeError(
                        node.end_node.position_start,
                        node.end_node.position_end,
                        "End index must be a number",
                        context,
                    )
                )

            end_index = int(end_value.value)

        if isinstance(object_to_slice, List):
            new_elements = [
                element.copy()
                for element in object_to_slice.elements[start_index:end_index]
            ]

            return result.success(
                List(new_elements)
                .set_context(context)
                .set_position(node.position_start, node.position_end)
            )
        elif isinstance(object_to_slice, String):
            return result.success(
                String(object_to_slice.value[start_index:end_index])
                .set_context(context)
                .set_position(node.position_start, node.position_end)
            )
        else:
            return result.failure(
                RuntimeError(
                    node.position_start,
                    node.position_end,
                    f"Type {type(object_to_slice).__name__} is not sliceable",
                    context,
                )
            )
