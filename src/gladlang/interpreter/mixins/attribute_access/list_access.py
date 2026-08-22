"""Visitors for subscript read and write (including compound assignment)."""

from gladlang.runtime.runtime_result import RuntimeResult


class InterpreterListAccess:
    def visit_ListAccessNode(self, node, context):
        result = RuntimeResult()

        list_value = result.register(self.visit(node.list_node, context))
        if result.error:
            return result

        index_value = result.register(self.visit(node.index_node, context))
        if result.error:
            return result

        element, error = list_value.get_element_at(index_value)
        if error:
            error.position_start = node.position_start
            error.position_end = node.position_end
            return result.failure(error)

        return result.success(
            element.set_position(node.position_start, node.position_end)
        )

    def visit_ListSetNode(self, node, context):
        result = RuntimeResult()

        list_value = result.register(self.visit(node.list_node, context))
        if result.error:
            return result

        index_value = result.register(self.visit(node.index_node, context))
        if result.error:
            return result

        if node.compound_operator is not None:
            old_value, error = list_value.get_element_at(index_value)
            if error:
                error.position_start = node.position_start
                error.position_end = node.position_end
                return result.failure(error)

            right_hand_side_value = result.register(
                self.visit(node.value_node, context)
            )

            if result.error:
                return result

            operator = self._binary_operator_dispatch.get(node.compound_operator)
            value_to_set, error = operator(old_value, right_hand_side_value)
            if error:
                return result.failure(error)
        else:
            value_to_set = result.register(self.visit(node.value_node, context))
            if result.error:
                return result

        new_value, error = list_value.set_element_at(index_value, value_to_set)
        if error:
            error.position_start = node.position_start
            error.position_end = node.position_end
            return result.failure(error)

        return result.success(new_value)
