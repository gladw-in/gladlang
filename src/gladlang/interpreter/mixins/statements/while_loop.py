"""Visitor for WHILE loops."""

from gladlang.runtime.context import Context
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.runtime.symbol_table import SymbolTable
from gladlang.values.primitives.number import Number


class InterpreterWhileLoop:
    def visit_WhileNode(self, while_node, context):
        result = RuntimeResult()

        while True:
            loop_context = Context("WHILE", context, while_node.position_start)
            loop_context.symbol_table = SymbolTable(context.symbol_table)
            condition_result = result.register(
                self.visit(while_node.condition_node, loop_context)
            )

            if result.error:
                return result

            if not condition_result.is_true():
                break

            body_result = result.register(
                self.visit(while_node.body_node, loop_context)
            )

            if result.error:
                return result

            if result.should_continue:
                result.should_continue = False
                continue

            if result.should_break:
                result.should_break = False
                break

            if result.should_return:
                return result

        return result.success(Number.null.copy())
