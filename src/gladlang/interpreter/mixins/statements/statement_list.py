"""Visitor for a sequential block of statements."""

from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number


class InterpreterStatementList:
    def visit_StatementListNode(self, node, context):
        result = RuntimeResult()

        last_value = Number.null.copy()

        for statement in node.statement_nodes:
            last_value = result.register(self.visit(statement, context))
            if (
                result.error
                or result.should_return
                or result.should_break
                or result.should_continue
            ):
                return result

        return result.success(last_value)
