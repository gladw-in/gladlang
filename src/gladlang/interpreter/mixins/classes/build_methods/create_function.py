"""Make a Function value from one method node of a class."""

from gladlang.values.functions.function import Function


class InterpreterBuildMethodsCreateFunction:
    def _create_method_function(self, method_node, context, class_value):
        method_name = method_node.variable_name_token.value
        return Function(
            method_name,
            method_node.body_node,
            method_node.argument_name_tokens,
            context,
            getattr(method_node, "visibility", "PUBLIC"),
            class_value,
            getattr(method_node, "is_static", False),
        ).set_position(method_node.position_start, method_node.position_end)
