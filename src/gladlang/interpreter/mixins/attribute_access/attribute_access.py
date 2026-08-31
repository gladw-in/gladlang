"""Visitors for attribute read and write (including compound assignment)."""

from gladlang.runtime.runtime_result import RuntimeResult


class InterpreterAttributeAccessCore:
    def visit_GetAttributeNode(self, node, context):
        result = RuntimeResult()

        instance = result.register(self.visit(node.object_node, context))
        if result.error:
            return result

        value, error = instance.get_attribute(node.attribute_name_token, context)
        if error:
            return result.failure(error)

        return result.success(
            value.set_position(node.position_start, node.position_end)
        )

    def visit_SetAttributeNode(self, node, context):
        result = RuntimeResult()

        instance = result.register(self.visit(node.object_node, context))
        if result.error:
            return result

        if node.compound_operator is not None:
            old_value, error = instance.get_attribute(
                node.attribute_name_token, context
            )
            if error:
                return result.failure(error)

            right_hand_side_value = result.register(
                self.visit(node.value_node, context)
            )

            if result.error:
                return result

            operator = self._binary_operator_dispatch.get(node.compound_operator)
            value, error = operator(old_value, right_hand_side_value)
            if error:
                return result.failure(error)
        else:
            value = result.register(self.visit(node.value_node, context))
            if result.error:
                return result

        new_value, error = instance.set_attribute(
            node.attribute_name_token, value, context
        )

        if error:
            return result.failure(error)

        return result.success(new_value)
