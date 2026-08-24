"""Visitor for the ternary conditional expression."""

from gladlang.runtime.runtime_result import RuntimeResult


class InterpreterTernary:
    def visit_TernaryOperatorNode(self, node, context):
        result = RuntimeResult()

        condition = result.register(self.visit(node.condition_node, context))
        if result.error:
            return result

        if condition.is_true():
            value = result.register(self.visit(node.true_case_node, context))
        else:
            value = result.register(self.visit(node.false_case_node, context))

        if result.error:
            return result

        return result.success(value)
