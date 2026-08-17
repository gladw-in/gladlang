"""Visitors for jump statements: BREAK, CONTINUE, RETURN (including tail-call return)."""

from gladlang.parser.ast import CallNode
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.nulls.tailcall import TailCall


class InterpreterJumpStatements:
    def visit_BreakNode(self, node, context):
        return RuntimeResult().success_break()

    def visit_ContinueNode(self, node, context):
        return RuntimeResult().success_continue()

    def visit_ReturnNode(self, node, context):
        result = RuntimeResult()

        tail_call_function = getattr(context, "_tco_func", None)
        if tail_call_function is not None and isinstance(node.node_to_return, CallNode):
            return_node = node.node_to_return
            function = result.register(self.visit(return_node.node_to_call, context))
            if result.error:
                return result

            tail_arguments = []
            for argument_node in return_node.argument_nodes:
                argument_value = result.register(self.visit(argument_node, context))
                if result.error:
                    return result

                tail_arguments.append(argument_value)

            return result.success_return(TailCall(function, tail_arguments))

        value = result.register(self.visit(node.node_to_return, context))
        if result.error:
            return result

        return result.success_return(value)
