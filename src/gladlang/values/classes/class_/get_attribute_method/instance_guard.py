"""Guards calling an instance method via the Class itself (constructor/parent/factory exceptions)."""

from gladlang.core.errors import RuntimeError


class ClassGetAttributeMethodInstanceGuard:
    __slots__ = ()

    def _check_instance_call_allowed(
        self, method_name, name_token, context, allow_instance
    ):
        is_constructor = method_name == self.name
        is_parent_method = (
            context and context.active_class and self in context.active_class.mro
        )

        is_factory_method = method_name == "get_instance" and self.name == "Singleton"

        if not allow_instance and not (
            is_constructor or is_parent_method or is_factory_method
        ):
            return RuntimeError(
                name_token.position_start,
                name_token.position_end,
                f"Instance method '{method_name}' cannot be called on the class '{self.name}'. Use an instance.",
                context,
            )

        return None
