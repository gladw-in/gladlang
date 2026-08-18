"""Visitor for call expressions: evaluates the callee and arguments, then executes."""

from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.classes.class_ import Class


class InterpreterCall:
    def visit_CallNode(self, node, context):
        result = RuntimeResult()

        arguments = []
        callee = result.register(self.visit(node.node_to_call, context))
        if result.error:
            return result

        callee = callee.set_position(node.position_start, node.position_end)
        if callee.context is None or isinstance(callee, Class):
            callee = callee.copy()
            callee.set_context(context)

        for argument_node in node.argument_nodes:
            arguments.append(result.register(self.visit(argument_node, context)))
            if result.error:
                return result

        return_value = result.register(callee.execute(arguments, self, context))
        if result.error:
            return result

        return result.success(return_value)
