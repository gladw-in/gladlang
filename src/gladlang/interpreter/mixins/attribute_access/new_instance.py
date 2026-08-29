"""Visitor for `NEW ClassName(arguments...)`."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.classes.class_ import Class


class InterpreterNewInstance:
    def visit_NewInstanceNode(self, node, context):
        result = RuntimeResult()

        class_name = node.class_name_token.value
        class_object = context.symbol_table.get(class_name)
        if not class_object:
            return result.failure(
                RuntimeError(
                    node.position_start,
                    node.position_end,
                    f"Class '{class_name}' is not defined",
                    context,
                )
            )

        if not isinstance(class_object, Class):
            return result.failure(
                RuntimeError(
                    node.position_start,
                    node.position_end,
                    f"'{class_name}' is not a class",
                    context,
                )
            )

        arguments = []
        for argument_node in node.argument_nodes:
            arguments.append(result.register(self.visit(argument_node, context)))
            if result.error:
                return result

        instance = result.register(
            class_object.instantiate(
                arguments,
                context,
                interpreter=self,
                call_position_start=node.position_start,
                call_position_end=node.position_end,
                calling_context=context,
            )
        )

        if result.error:
            return result

        return result.success(
            instance.set_position(node.position_start, node.position_end).set_context(
                context
            )
        )
