"""Visitor for function definitions."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.functions.function import Function
from gladlang.values.functions.function_group import FunctionGroup


class InterpreterFunctions:
    def visit_FunctionDefinitionNode(self, node, context):
        result = RuntimeResult()

        function_name = (
            node.variable_name_token.value if node.variable_name_token else None
        )
        defining_class = context.active_class

        function = Function(
            function_name,
            node.body_node,
            node.argument_name_tokens,
            context,
            visibility=getattr(node, "visibility", "PUBLIC"),
            defining_class=defining_class,
            is_static=getattr(node, "is_static", False),
        )

        if function_name:
            if function_name in context.symbol_table.finals:
                return result.failure(
                    RuntimeError(
                        node.position_start,
                        node.position_end,
                        f"Cannot override constant '{function_name}' with a function definition",
                        context,
                    )
                )

            existing_value = context.symbol_table.get(function_name)

            if existing_value is not None:
                if isinstance(existing_value, FunctionGroup):
                    argument_count = len(function.argument_names)
                    if argument_count in existing_value.functions:
                        existing_value.functions[argument_count] = function
                    else:
                        error = existing_value.add_function(function)
                        if error and isinstance(error, RuntimeResult) and error.error:
                            return error

                    function = existing_value

                elif isinstance(existing_value, Function):
                    existing_argument_count = len(existing_value.argument_names)
                    new_argument_count = len(function.argument_names)
                    if existing_argument_count == new_argument_count:
                        context.symbol_table.set(function_name, function)
                    else:
                        function_group = FunctionGroup(function_name)
                        function_group.add_function(existing_value)
                        error = function_group.add_function(function)
                        if error and isinstance(error, RuntimeResult) and error.error:
                            return error

                        context.symbol_table.set(function_name, function_group)
                        function = function_group
                else:
                    context.symbol_table.set(function_name, function)
            else:
                context.symbol_table.set(function_name, function)

        return result.success(
            function.set_position(node.position_start, node.position_end).set_context(
                context
            )
        )
