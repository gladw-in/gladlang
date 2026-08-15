"""Core Function machinery: slots, construction, binding to an instance, and copy."""

from gladlang.values.functions.base_function import BaseFunction


class FunctionCore(BaseFunction):
    __slots__ = (
        "body_node",
        "argument_name_tokens",
        "argument_names",
        "context",
        "visibility",
        "defining_class",
        "is_static",
        "_call_count",
    )

    def __init__(
        self,
        name,
        body_node,
        argument_name_tokens,
        parent_context,
        visibility="PUBLIC",
        defining_class=None,
        is_static=False,
    ):
        super().__init__(name)
        self.body_node = body_node
        self.argument_name_tokens = argument_name_tokens
        self.argument_names = [token.value for token in argument_name_tokens]
        self.context = parent_context
        self.visibility = visibility
        self.defining_class = defining_class
        self.is_static = is_static
        self._call_count = 0

    def bind_to_instance(self, instance):
        from gladlang.values.functions.bound_method import BoundMethod

        return BoundMethod(self.name, self, instance)

    def copy(self):
        from gladlang.values.functions.function import Function

        function_copy = Function(
            self.name,
            self.body_node,
            self.argument_name_tokens,
            self.context,
            self.visibility,
            self.defining_class,
            self.is_static,
        )

        function_copy.set_position(self.position_start, self.position_end)
        function_copy.set_context(self.context)

        return function_copy
