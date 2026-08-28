"""Visitor for iterator-style FOR loops: FOR x IN iterable ... ENDFOR."""

from gladlang.runtime.context import Context
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.runtime.symbol_table import SymbolTable
from gladlang.values.primitives.number import Number


class InterpreterForLoop:
    def visit_ForNode(self, node, context):
        result = RuntimeResult()

        iterable = result.register(self.visit(node.iterable_node, context))
        if result.error:
            return result

        iterator, error = self.get_iterator(
            iterable,
            node.iterable_node.position_start,
            node.iterable_node.position_end,
            context,
        )

        if error:
            return result.failure(error)

        for element in iterator:
            for_context = Context("FOR", context, node.position_start)
            for_context.symbol_table = SymbolTable(context.symbol_table)
            self.unpack_and_set(node.var_name_tokens, element, for_context, result)
            if result.error:
                return result

            body_result = result.register(self.visit(node.body_node, for_context))
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
