"""Visitor for dict comprehensions."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.context import Context
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.runtime.symbol_table import SymbolTable
from gladlang.values.primitives.dict import Dict
from gladlang.values.primitives.number import Number
from gladlang.values.primitives.string import String


class InterpreterDictComprehension:
    def visit_DictComprehensionNode(self, node, context):
        result = RuntimeResult()

        output_dictionary = {}

        def evaluate_loops(specification_index, comprehension_context):
            if specification_index >= len(node.iteration_specifications):
                key_value = result.register(
                    self.visit(node.key_expression_node, comprehension_context)
                )

                if result.error:
                    return

                value_value = result.register(
                    self.visit(node.value_expression_node, comprehension_context)
                )

                if result.error:
                    return

                if isinstance(key_value, (Number, String)):
                    output_dictionary[key_value.value] = value_value
                else:
                    result.failure(
                        RuntimeError(
                            node.key_expression_node.position_start,
                            node.key_expression_node.position_end,
                            "Dictionary key must be a Number or String",
                            comprehension_context,
                        )
                    )
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
                    "DICT_COMPREHENSION", comprehension_context, node.position_start
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

        base_context = Context("DICT_COMPREHENSION", context, node.position_start)
        base_context.symbol_table = SymbolTable(context.symbol_table)

        evaluate_loops(0, base_context)
        if result.error:
            return result

        return result.success(
            Dict(output_dictionary)
            .set_context(context)
            .set_position(node.position_start, node.position_end)
        )
