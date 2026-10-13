"""List literal visitor."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.list import List


class InterpreterListLiteralsListLiteral:
    def visit_ListNode(self, node, context):
        result = RuntimeResult()

        elements = []
        for element_node in node.element_nodes:
            if len(elements) >= Settings.MAX_LIST_SIZE:
                return result.failure(
                    RuntimeError(
                        node.position_start,
                        node.position_end,
                        f"List literal exceeds maximum allowed size "
                        f"({Settings.MAX_LIST_SIZE:,})",
                        context,
                    )
                )

            elements.append(result.register(self.visit(element_node, context)))
            if result.error:
                return result

        return result.success(
            List(elements)
            .set_context(context)
            .set_position(node.position_start, node.position_end)
        )
