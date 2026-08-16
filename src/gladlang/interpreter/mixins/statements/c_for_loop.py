"""Visitor for C-style FOR loops: FOR (init; condition; step) ... ENDFOR."""

from gladlang.runtime.context import Context
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.runtime.symbol_table import SymbolTable
from gladlang.values.primitives.number import Number


class InterpreterCForLoop:
    def visit_CForNode(self, node, context):
        result = RuntimeResult()

        for_context = Context("C_FOR", context, node.position_start)
        for_context.symbol_table = SymbolTable(context.symbol_table)
        for_context.active_class = context.active_class

        if node.init_node:
            result.register(self.visit(node.init_node, for_context))
            if result.error:
                return result

        while True:
            if node.condition_node:
                condition_result = result.register(
                    self.visit(node.condition_node, for_context)
                )

                if result.error:
                    return result

                if not condition_result.is_true():
                    break

            iteration_context = Context("C_FOR", context, node.position_start)
            iteration_symbol_table = for_context.symbol_table.copy()
            iteration_context.symbol_table = iteration_symbol_table
            iteration_context.active_class = context.active_class

            result.register(self.visit(node.body_node, iteration_context))
            if result.error:
                return result

            for key, value in iteration_symbol_table.symbols.items():
                if key in for_context.symbol_table.symbols:
                    for_context.symbol_table.symbols[key] = value

            if result.should_continue:
                result.should_continue = False
            elif result.should_break:
                result.should_break = False
                break
            elif result.should_return:
                return result

            if node.step_node:
                result.register(self.visit(node.step_node, for_context))
                if result.error:
                    return result

        return result.success(Number.null.copy())
