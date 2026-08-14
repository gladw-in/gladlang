"""Visitor for PRINT / PRINTLN statements."""

import sys

from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number


class InterpreterPrintStatement:
    def visit_PrintNode(self, node, context):
        result = RuntimeResult()

        parts = []
        for item in node.print_nodes:
            value = result.register(self.visit(item, context))
            if result.error:
                return result

            parts.append(str(value))

        output = " ".join(parts)
        if node.should_newline:
            output += "\n"

        sys.stdout.write(output)
        if not node.should_newline:
            sys.stdout.flush()

        return result.success(Number.null.copy())
