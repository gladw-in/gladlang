"""List comprehension visitor."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings
from gladlang.runtime.context import Context
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.runtime.symbol_table import SymbolTable
from gladlang.values.primitives.list import List


class InterpreterListLiteralsListComprehension:
    def visit_ListComprehensionNode(self, node, context):
        result = RuntimeResult()

        output_list = []

        def evaluate_loops(specification_index, comprehension_context):
            if specification_index >= len(node.iteration_specifications):
                value = result.register(
                    self.visit(node.output_expression_node, comprehension_context)
                )

                if not result.error:
                    if len(output_list) >= Settings.MAX_LIST_SIZE:
                        result.failure(
                            RuntimeError(
                                node.position_start,
                                node.position_end,
                                f"List comprehension exceeds maximum allowed size "
                                f"({Settings.MAX_LIST_SIZE:,})",
                                comprehension_context,
                            )
                        )
                        return

                    output_list.append(value)

                return

            variable_tokens, iterable_node, condition_node = (
                node.iteration_specifications[specification_index]
            )

            iterable_value = result.register(
                self.visit(iterable_node, comprehension_context)
            )

            if result.error:
                return

            iterator, error = self.get_iterator(
                iterable_value,
                iterable_node.position_start,
                iterable_node.position_end,
                context,
            )

            if error:
                result.failure(error)
                return

            for element in iterator:
                iteration_context = Context(
                    "LIST_COMPREHENSION", comprehension_context, node.position_start
                )

                iteration_context.symbol_table = SymbolTable(
                    comprehension_context.symbol_table
                )

                self.unpack_and_set(variable_tokens, element, iteration_context, result)
                if result.error:
                    return

                if condition_node:
                    condition_value = result.register(
                        self.visit(condition_node, iteration_context)
                    )

                    if result.error:
                        return

                    if not condition_value.is_true():
                        continue

                evaluate_loops(specification_index + 1, iteration_context)
                if result.error:
                    return

        base_context = Context("LIST_COMPREHENSION", context, node.position_start)
        base_context.symbol_table = SymbolTable(context.symbol_table)

        evaluate_loops(0, base_context)
        if result.error:
            return result

        return result.success(
            List(output_list)
            .set_context(context)
            .set_position(node.position_start, node.position_end)
        )
