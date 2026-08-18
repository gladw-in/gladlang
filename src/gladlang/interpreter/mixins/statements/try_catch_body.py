"""Helper that runs TRY body and CATCH on error, capturing return/break/continue/value."""

from gladlang.runtime.context import Context
from gladlang.runtime.symbol_table import SymbolTable
from gladlang.values.primitives.string import String


class InterpreterTryCatchBody:
    def _run_try_catch_body(self, node, context):
        try_result = self.visit(node.try_body_node, context)

        captured_error = None
        captured_return_value = None
        captured_should_return = False
        captured_break = False
        captured_continue = False
        captured_value = None

        if try_result.error:
            if node.catch_body_node:
                catch_context = Context("CATCH", context, node.position_start)
                catch_context.symbol_table = SymbolTable(context.symbol_table)

                if node.catch_variable_node:
                    error_message = try_result.error.details
                    error_value = getattr(try_result.error, "thrown_value", None)

                    if error_value is None:
                        error_value = String(error_message)

                    catch_context.symbol_table.set(
                        node.catch_variable_node.value, error_value
                    )

                catch_result = self.visit(node.catch_body_node, catch_context)
                if catch_result.error:
                    captured_error = catch_result.error
                elif catch_result.should_return:
                    captured_should_return = True
                    captured_return_value = catch_result.return_value
                elif catch_result.should_break:
                    captured_break = True
                elif catch_result.should_continue:
                    captured_continue = True
                else:
                    captured_value = catch_result.value

            else:
                captured_error = try_result.error
        else:
            if try_result.should_return:
                captured_should_return = True
                captured_return_value = try_result.return_value
            elif try_result.should_break:
                captured_break = True
            elif try_result.should_continue:
                captured_continue = True
            else:
                captured_value = try_result.value

        return (
            captured_error,
            captured_should_return,
            captured_return_value,
            captured_break,
            captured_continue,
            captured_value,
        )
