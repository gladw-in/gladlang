"""Visitors for TRY/CATCH/FINALLY (outer control flow + FINALLY semantics) and THROW."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.context import Context
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.runtime.symbol_table import SymbolTable
from gladlang.values.primitives.number import Number


class InterpreterTryCatch:
    def visit_TryCatchNode(self, try_catch_node, context):
        result = RuntimeResult()

        (
            captured_error,
            captured_should_return,
            captured_return_value,
            captured_break,
            captured_continue,
            captured_value,
        ) = self._run_try_catch_body(try_catch_node, context)

        if try_catch_node.finally_body_node:
            finally_context = Context("FINALLY", context, try_catch_node.position_start)
            finally_context.symbol_table = SymbolTable(context.symbol_table)
            finally_context.active_class = context.active_class
            finally_result = self.visit(
                try_catch_node.finally_body_node, finally_context
            )

            if finally_result.error:
                return finally_result

            if finally_result.should_return:
                return finally_result

            if finally_result.should_break:
                return RuntimeResult().success_break()

            if finally_result.should_continue:
                return RuntimeResult().success_continue()

        if captured_error:
            return RuntimeResult().failure(captured_error)

        if captured_should_return:
            return RuntimeResult().success_return(captured_return_value)

        if captured_break:
            return RuntimeResult().success_break()

        if captured_continue:
            return RuntimeResult().success_continue()

        if captured_value is not None:
            return result.success(captured_value)

        return result.success(Number.null.copy())

    def visit_ThrowNode(self, throw_node, context):
        result = RuntimeResult()

        thrown_value = result.register(self.visit(throw_node.node_to_throw, context))
        if result.error:
            return result

        return result.failure(
            RuntimeError(
                throw_node.position_start,
                throw_node.position_end,
                str(thrown_value),
                context,
                thrown_value=thrown_value,
            )
        )
