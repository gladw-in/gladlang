"""Core BoundMethod machinery: slots, construction, rebinding, and copy."""

from gladlang.values.functions.base_function import BaseFunction


class BoundMethodCore(BaseFunction):
    __slots__ = (
        "function_to_bind",
        "instance",
        "context",
        "visibility",
        "defining_class",
        "is_static",
        "_call_count",
    )

    def __init__(self, name, function_to_bind, instance):
        super().__init__(name)
        self.function_to_bind = function_to_bind
        self.instance = instance
        self.context = function_to_bind.context
        self.set_position(
            function_to_bind.position_start, function_to_bind.position_end
        )
        self.visibility = getattr(function_to_bind, "visibility", "PUBLIC")
        self.defining_class = getattr(function_to_bind, "defining_class", None)
        self.is_static = getattr(function_to_bind, "is_static", False)
        self._call_count = 0

    def bind_to_instance(self, instance):
        from gladlang.values.functions.bound_method import BoundMethod

        return BoundMethod(self.name, self.function_to_bind, instance)

    def copy(self):
        from gladlang.values.functions.bound_method import BoundMethod

        bound_method_copy = (
            BoundMethod(self.name, self.function_to_bind.copy(), self.instance)
            .set_context(self.context)
            .set_position(self.position_start, self.position_end)
        )

        return bound_method_copy
